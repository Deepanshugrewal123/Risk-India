/**
 * RISK // INDIA — Resilient HTTP API Client
 * 
 * Production-grade API client providing:
 * - Explicit configurable request timeouts via AbortController
 * - Safe error normalization without leaking internals
 * - Network failure detection
 * - Strict retry discipline: GET requests allow 1 bounded retry with backoff;
 *   POST / analytical requests strictly allow ZERO automatic retries to prevent backend overload.
 */

export class ApiError extends Error {
  public status?: number;
  public statusText?: string;
  public isTimeout: boolean;
  public isNetworkError: boolean;
  public details?: any;

  constructor(message: string, options?: {
    status?: number;
    statusText?: string;
    isTimeout?: boolean;
    isNetworkError?: boolean;
    details?: any;
  }) {
    super(message);
    this.name = 'ApiError';
    this.status = options?.status;
    this.statusText = options?.statusText;
    this.isTimeout = Boolean(options?.isTimeout);
    this.isNetworkError = Boolean(options?.isNetworkError);
    this.details = options?.details;
  }
}

export interface RequestOptions extends RequestInit {
  timeoutMs?: number;
  retries?: number;
  retryDelayMs?: number;
}

const DEFAULT_TIMEOUT_MS = 8000;

/**
 * Execute an HTTP fetch request with AbortController timeout and bounded retries.
 */
export async function requestWithTimeout<T = any>(
  url: string,
  options: RequestOptions = {}
): Promise<T> {
  const method = (options.method || 'GET').toUpperCase();
  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  // Strictly disallow retries on non-GET / non-HEAD requests
  const maxRetries = (method === 'GET' || method === 'HEAD') ? Math.min(options.retries ?? 1, 1) : 0;
  const retryDelayMs = options.retryDelayMs ?? 500;

  let attempt = 0;

  while (true) {
    const controller = new AbortController();
    const timer = setTimeout(() => {
      controller.abort();
    }, timeoutMs);

    try {
      // Check offline status before attempting fetch
      if (typeof navigator !== 'undefined' && !navigator.onLine) {
        throw new ApiError('Browser is currently offline. Showing cached information.', {
          isNetworkError: true
        });
      }

      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });

      clearTimeout(timer);

      if (!response.ok) {
        let errData: any = null;
        try {
          errData = await response.json();
        } catch {
          // Response was not JSON
        }

        const message = errData?.detail || errData?.message || `HTTP ${response.status}: ${response.statusText}`;
        throw new ApiError(message, {
          status: response.status,
          statusText: response.statusText,
          details: errData
        });
      }

      return (await response.json()) as T;
    } catch (err: any) {
      clearTimeout(timer);

      const isAbort = err?.name === 'AbortError' || controller.signal.aborted;
      const isNetwork = err instanceof ApiError ? err.isNetworkError : (
        err?.message?.includes('Failed to fetch') ||
        err?.message?.includes('NetworkError') ||
        err?.name === 'TypeError'
      );

      const normalizedError = isAbort
        ? new ApiError(`Request to ${url} timed out after ${timeoutMs}ms.`, { isTimeout: true })
        : err instanceof ApiError
        ? err
        : new ApiError(err?.message || 'Network communication error', {
            isNetworkError: isNetwork
          });

      // Check if retry is permissible
      attempt++;
      if (attempt <= maxRetries && (normalizedError.isTimeout || normalizedError.isNetworkError)) {
        await new Promise((res) => setTimeout(res, retryDelayMs * attempt));
        continue;
      }

      throw normalizedError;
    }
  }
}

/**
 * Convenient typed API wrappers
 */
export const apiClient = {
  get: <T = any>(url: string, options?: RequestOptions): Promise<T> => {
    return requestWithTimeout<T>(url, { ...options, method: 'GET' });
  },

  post: <T = any>(url: string, body?: any, options?: RequestOptions): Promise<T> => {
    return requestWithTimeout<T>(url, {
      ...options,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(options?.headers || {})
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
      // Strictly 0 retries on POST
      retries: 0
    });
  }
};

export default apiClient;
