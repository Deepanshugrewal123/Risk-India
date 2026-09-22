import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertCircle, RotateCcw, Home } from 'lucide-react';

interface ErrorBoundaryProps {
  children: ReactNode;
  fallbackTitle?: string;
  fallbackMessage?: string;
  onReset?: () => void;
}

interface ErrorBoundaryState {
  hasError: boolean;
  errorId: string;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      errorId: ''
    };
  }

  static getDerivedStateFromError(_: Error): ErrorBoundaryState {
    // Generate a safe non-sensitive incident reference
    const ref = `ERR-${Math.random().toString(36).substring(2, 8).toUpperCase()}`;
    return {
      hasError: true,
      errorId: ref
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Log sanitized diagnostic details to console without leaking to UI
    console.error('[RISK//INDIA ErrorBoundary caught unhandled error]', {
      name: error?.name,
      message: error?.message,
      componentStack: errorInfo?.componentStack?.slice(0, 300)
    });
  }

  handleReset = (): void => {
    if (this.props.onReset) {
      this.props.onReset();
    }
    this.setState({ hasError: false, errorId: '' });
  };

  handleReload = (): void => {
    if (typeof window !== 'undefined') {
      window.location.reload();
    }
  };

  handleNavigateHome = (): void => {
    if (typeof window !== 'undefined') {
      window.location.href = '/';
    }
  };

  render(): ReactNode {
    if (this.state.hasError) {
      const title = this.props.fallbackTitle || 'Interface Render Notice';
      const message =
        this.props.fallbackMessage ||
        'An unexpected display issue occurred while rendering this section. Essential emergency resources, disaster hotlines, and maps remain operational.';

      return (
        <div className="min-h-[420px] w-full flex items-center justify-center p-6 bg-paper-100 text-charcoal-900">
          <div className="max-w-md w-full bg-white border border-paper-300 rounded-3xl p-8 shadow-elevated text-center transition-all duration-300 motion-reduce:transition-none">
            {/* Header Icon */}
            <div className="w-12 h-12 mx-auto mb-5 rounded-2xl bg-amber-50 border border-amber-200/60 flex items-center justify-center text-amber-700">
              <AlertCircle className="w-6 h-6" />
            </div>

            {/* Badge */}
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-paper-100 border border-paper-300 text-charcoal-600 text-[11px] font-mono mb-3">
              <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
              <span>SAFETY FALLBACK • {this.state.errorId}</span>
            </div>

            {/* Content */}
            <h3 className="text-xl font-bold text-charcoal-900 tracking-tight mb-2">
              {title}
            </h3>
            <p className="text-sm text-charcoal-600 leading-relaxed mb-6 font-normal">
              {message}
            </p>

            {/* Emergency Hotline reminder */}
            <div className="bg-paper-50 border border-paper-200 rounded-2xl p-3.5 mb-6 text-left">
              <p className="text-[11px] uppercase tracking-wider font-mono text-charcoal-500 font-semibold mb-1">
                National Emergency Direct Access
              </p>
              <div className="flex items-center justify-between text-xs text-charcoal-800">
                <span>Pan-India Emergency Response</span>
                <a
                  href="tel:112"
                  className="font-mono font-bold text-rose-600 hover:text-rose-700 underline"
                >
                  Dial 112
                </a>
              </div>
            </div>

            {/* Actions */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-2.5">
              <button
                type="button"
                onClick={this.handleReset}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-charcoal-900 text-paper-50 hover:bg-charcoal-800 text-xs font-semibold tracking-wide transition-all shadow-subtle active:scale-95 motion-reduce:active:scale-100"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Try Again</span>
              </button>

              <button
                type="button"
                onClick={this.handleReload}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-paper-100 hover:bg-paper-200 text-charcoal-700 text-xs font-semibold tracking-wide transition-all border border-paper-300 active:scale-95 motion-reduce:active:scale-100"
              >
                <span>Reload Page</span>
              </button>

              <button
                type="button"
                onClick={this.handleNavigateHome}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl text-charcoal-500 hover:text-charcoal-800 text-xs font-medium tracking-wide transition-colors"
                title="Return to Homepage"
              >
                <Home className="w-3.5 h-3.5" />
                <span>Home</span>
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
