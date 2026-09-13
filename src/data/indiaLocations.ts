import { IndiaLocation } from '../types/location';

export const ALL_INDIAN_STATES: IndiaLocation[] = [
  {
    id: 'andhra-pradesh',
    name: 'Andhra Pradesh',
    type: 'STATE',
    code: 'AP',
    capital: 'Amaravati',
    region: 'South India',
    latitude: 15.9129,
    longitude: 79.7400,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Flood',
    riskScore: 72,
    districts: [
      'Visakhapatnam', 'East Godavari', 'West Godavari', 'Krishna', 'Guntur',
      'Nellore', 'Srikakulam', 'Vizianagaram', 'Prakasam', 'Kurnool',
      'Anantapur', 'Kadapa', 'Chittoor', 'Tirupati', 'Kakinada'
    ],
    isDemoData: true
  },
  {
    id: 'arunachal-pradesh',
    name: 'Arunachal Pradesh',
    type: 'STATE',
    code: 'AR',
    capital: 'Itanagar',
    region: 'Northeast India',
    latitude: 28.2180,
    longitude: 94.7278,
    primaryRisk: 'Landslide',
    secondaryRisk: 'Earthquake',
    riskScore: 78,
    districts: [
      'Papum Pare (Itanagar)', 'Tawang', 'West Kameng', 'East Kameng', 'Lower Subansiri',
      'Upper Subansiri', 'West Siang', 'East Siang', 'Dibang Valley', 'Lohit',
      'Changlang', 'Tirap', 'Anjaw', 'Kurung Kumey', 'Shi Yomi'
    ],
    isDemoData: true
  },
  {
    id: 'assam',
    name: 'Assam',
    type: 'STATE',
    code: 'AS',
    capital: 'Dispur',
    region: 'Northeast India',
    latitude: 26.1445,
    longitude: 91.7362,
    primaryRisk: 'Flood',
    secondaryRisk: 'Landslide',
    riskScore: 84,
    districts: [
      'Udalguri', 'Darrang', 'Guwahati (Kamrup Metro)', 'Kamrup Rural', 'Dhubri', 'Barpeta', 'Nagaon',
      'Morigaon', 'Cachar', 'Golaghat', 'Dibrugarh', 'Silchar',
      'Sonitpur', 'Lakhimpur', 'Dhemaji', 'Jorhat', 'Sivasagar'
    ],
    isDemoData: true
  },
  {
    id: 'bihar',
    name: 'Bihar',
    type: 'STATE',
    code: 'BR',
    capital: 'Patna',
    region: 'East India',
    latitude: 25.0961,
    longitude: 85.3131,
    primaryRisk: 'Flood',
    secondaryRisk: 'Heatwave',
    riskScore: 82,
    districts: [
      'Patna', 'Muzaffarpur', 'Darbhanga', 'Bhagalpur', 'Supaul',
      'Saharsa', 'Khagaria', 'Katihar', 'Purnia', 'Gaya',
      'Madhubani', 'Samastipur', 'Begusarai', 'Vaishali', 'Rohtas'
    ],
    isDemoData: true
  },
  {
    id: 'chhattisgarh',
    name: 'Chhattisgarh',
    type: 'STATE',
    code: 'CG',
    capital: 'Raipur',
    region: 'Central India',
    latitude: 21.2787,
    longitude: 81.8661,
    primaryRisk: 'Heatwave',
    secondaryRisk: 'Drought',
    riskScore: 56,
    districts: [
      'Raipur', 'Bilaspur', 'Durg', 'Bastar (Jagdalpur)', 'Rajnandgaon',
      'Korba', 'Raigarh', 'Surguja', 'Dhamtari', 'Mahasamund',
      'Janjgir-Champa', 'Kanker', 'Kawardha', 'Sukma', 'Bijapur'
    ],
    isDemoData: true
  },
  {
    id: 'goa',
    name: 'Goa',
    type: 'STATE',
    code: 'GA',
    capital: 'Panaji',
    region: 'West India',
    latitude: 15.2993,
    longitude: 74.1240,
    primaryRisk: 'Flood',
    secondaryRisk: 'Cyclone',
    riskScore: 48,
    districts: [
      'North Goa (Panaji)', 'South Goa (Margao)', 'Bardez (Mapusa)',
      'Salcete', 'Ponda', 'Tiswadi', 'Mormugao', 'Bicholim'
    ],
    isDemoData: true
  },
  {
    id: 'gujarat',
    name: 'Gujarat',
    type: 'STATE',
    code: 'GJ',
    capital: 'Gandhinagar',
    region: 'West India',
    latitude: 22.2587,
    longitude: 71.1924,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Earthquake',
    riskScore: 76,
    districts: [
      'Kutch', 'Jamnagar', 'Junagadh', 'Porbandar', 'Surat',
      'Ahmedabad', 'Bhavnagar', 'Morbi', 'Rajkot', 'Vadodara',
      'Amreli', 'Gir Somnath', 'Navsari', 'Valsad', 'Patan'
    ],
    isDemoData: true
  },
  {
    id: 'haryana',
    name: 'Haryana',
    type: 'STATE',
    code: 'HR',
    capital: 'Chandigarh',
    region: 'North India',
    latitude: 29.0588,
    longitude: 76.0856,
    primaryRisk: 'Heatwave',
    secondaryRisk: 'Flood',
    riskScore: 58,
    districts: [
      'Gurugram', 'Faridabad', 'Ambala', 'Panchkula', 'Karnal',
      'Panipat', 'Sonipat', 'Rohtak', 'Hisar', 'Sirsa',
      'Yamunanagar', 'Kurukshetra', 'Rewari', 'Jhajjar', 'Bhiwani'
    ],
    isDemoData: true
  },
  {
    id: 'himachal-pradesh',
    name: 'Himachal Pradesh',
    type: 'STATE',
    code: 'HP',
    capital: 'Shimla',
    region: 'North India',
    latitude: 31.1048,
    longitude: 77.1734,
    primaryRisk: 'Landslide',
    secondaryRisk: 'Flood',
    riskScore: 91,
    districts: [
      'Shimla', 'Mandi', 'Kullu', 'Kangra (Dharamshala)', 'Kinnaur',
      'Lahaul & Spiti', 'Solan', 'Chamba', 'Sirmaur', 'Bilaspur',
      'Hamirpur', 'Una'
    ],
    isDemoData: true
  },
  {
    id: 'jharkhand',
    name: 'Jharkhand',
    type: 'STATE',
    code: 'JH',
    capital: 'Ranchi',
    region: 'East India',
    latitude: 23.6102,
    longitude: 85.2799,
    primaryRisk: 'Drought',
    secondaryRisk: 'Heatwave',
    riskScore: 61,
    districts: [
      'Ranchi', 'East Singhbhum (Jamshedpur)', 'Dhanbad', 'Bokaro', 'Hazaribagh',
      'Deoghar', 'Giridih', 'Palamu', 'Ramgarh', 'Dumka',
      'Chaibasa', 'Garhwa', 'Koderma', 'Latehar', 'Sahebganj'
    ],
    isDemoData: true
  },
  {
    id: 'karnataka',
    name: 'Karnataka',
    type: 'STATE',
    code: 'KA',
    capital: 'Bengaluru',
    region: 'South India',
    latitude: 15.3173,
    longitude: 75.7139,
    primaryRisk: 'Drought',
    secondaryRisk: 'Flood',
    riskScore: 64,
    districts: [
      'Bengaluru Urban', 'Bengaluru Rural', 'Kodagu (Coorg)', 'Dakshina Kannada (Mangaluru)',
      'Udupi', 'Uttara Kannada', 'Belagavi', 'Mysuru', 'Ballari',
      'Shivamogga', 'Chikkamagaluru', 'Kalaburagi', 'Dharwad', 'Tumakuru', 'Vijayapura'
    ],
    isDemoData: true
  },
  {
    id: 'kerala',
    name: 'Kerala',
    type: 'STATE',
    code: 'KL',
    capital: 'Thiruvananthapuram',
    region: 'South India',
    latitude: 10.8505,
    longitude: 76.2711,
    primaryRisk: 'Landslide',
    secondaryRisk: 'Flood',
    riskScore: 86,
    districts: [
      'Wayanad', 'Idukki', 'Ernakulam (Kochi)', 'Alappuzha', 'Pathanamthitta',
      'Kottayam', 'Thrissur', 'Kozhikode', 'Thiruvananthapuram', 'Palakkad',
      'Malappuram', 'Kannur', 'Kasaragod', 'Kollam'
    ],
    isDemoData: true
  },
  {
    id: 'madhya-pradesh',
    name: 'Madhya Pradesh',
    type: 'STATE',
    code: 'MP',
    capital: 'Bhopal',
    region: 'Central India',
    latitude: 22.9734,
    longitude: 78.6569,
    primaryRisk: 'Heatwave',
    secondaryRisk: 'Flood',
    riskScore: 59,
    districts: [
      'Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain',
      'Sagar', 'Rewa', 'Satna', 'Hoshangabad (Narmadapuram)', 'Chhindwara',
      'Ratlam', 'Vidisha', 'Sehore', 'Dewas', 'Shivpuri'
    ],
    isDemoData: true
  },
  {
    id: 'maharashtra',
    name: 'Maharashtra',
    type: 'STATE',
    code: 'MH',
    capital: 'Mumbai',
    region: 'West India',
    latitude: 19.7515,
    longitude: 75.7139,
    primaryRisk: 'Flood',
    secondaryRisk: 'Drought',
    riskScore: 79,
    districts: [
      'Mumbai', 'Mumbai Suburban', 'Thane', 'Raigad', 'Ratnagiri',
      'Sindhudurg', 'Pune', 'Kolhapur', 'Sangli', 'Satara',
      'Nashik', 'Nagpur', 'Aurangabad (Chhatrapati Sambhajinagar)', 'Solapur', 'Amravati'
    ],
    isDemoData: true
  },
  {
    id: 'manipur',
    name: 'Manipur',
    type: 'STATE',
    code: 'MN',
    capital: 'Imphal',
    region: 'Northeast India',
    latitude: 24.6637,
    longitude: 93.9063,
    primaryRisk: 'Earthquake',
    secondaryRisk: 'Landslide',
    riskScore: 71,
    districts: [
      'Imphal West', 'Imphal East', 'Churachandpur', 'Bishnupur', 'Thoubal',
      'Ukhrul', 'Senapati', 'Tamenglong', 'Chandel', 'Kangpokpi'
    ],
    isDemoData: true
  },
  {
    id: 'meghalaya',
    name: 'Meghalaya',
    type: 'STATE',
    code: 'ML',
    capital: 'Shillong',
    region: 'Northeast India',
    latitude: 25.4670,
    longitude: 91.3662,
    primaryRisk: 'Flood',
    secondaryRisk: 'Landslide',
    riskScore: 80,
    districts: [
      'East Khasi Hills (Shillong)', 'West Khasi Hills', 'South West Khasi Hills',
      'Ri-Bhoi', 'West Garo Hills (Tura)', 'East Garo Hills', 'South Garo Hills',
      'West Jaintia Hills', 'East Jaintia Hills'
    ],
    isDemoData: true
  },
  {
    id: 'mizoram',
    name: 'Mizoram',
    type: 'STATE',
    code: 'MZ',
    capital: 'Aizawl',
    region: 'Northeast India',
    latitude: 23.1645,
    longitude: 92.9376,
    primaryRisk: 'Landslide',
    secondaryRisk: 'Earthquake',
    riskScore: 74,
    districts: [
      'Aizawl', 'Lunglei', 'Champhai', 'Kolasib', 'Serchhip',
      'Lawngtlai', 'Mamit', 'Saiha', 'Hnahthial', 'Khawzawl'
    ],
    isDemoData: true
  },
  {
    id: 'nagaland',
    name: 'Nagaland',
    type: 'STATE',
    code: 'NL',
    capital: 'Kohima',
    region: 'Northeast India',
    latitude: 26.1584,
    longitude: 94.5624,
    primaryRisk: 'Earthquake',
    secondaryRisk: 'Landslide',
    riskScore: 73,
    districts: [
      'Kohima', 'Dimapur', 'Mokokchung', 'Wokha', 'Mon',
      'Phek', 'Zunheboto', 'Tuensang', 'Longleng', 'Kiphire', 'Peren', 'Chümoukedima'
    ],
    isDemoData: true
  },
  {
    id: 'odisha',
    name: 'Odisha',
    type: 'STATE',
    code: 'OD',
    capital: 'Bhubaneswar',
    region: 'East India',
    latitude: 20.9517,
    longitude: 85.0985,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Flood',
    riskScore: 68,
    districts: [
      'Puri', 'Bhubaneswar (Khurda)', 'Cuttack', 'Balasore', 'Ganjam',
      'Jagatsinghpur', 'Kendrapara', 'Bhadrak', 'Mayurbhanj', 'Jajpur',
      'Sambalpur', 'Koraput', 'Bargarh', 'Rayagada', 'Sundargarh'
    ],
    isDemoData: true
  },
  {
    id: 'punjab',
    name: 'Punjab',
    type: 'STATE',
    code: 'PB',
    capital: 'Chandigarh',
    region: 'North India',
    latitude: 31.1471,
    longitude: 75.3412,
    primaryRisk: 'Flood',
    secondaryRisk: 'Heatwave',
    riskScore: 62,
    districts: [
      'Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda',
      'Hoshiarpur', 'Rupnagar (Ropar)', 'Gurdaspur', 'Firozpur', 'Fazilka',
      'Mohali (SAS Nagar)', 'Sangrur', 'Moga', 'Kapurthala', 'Pathankot'
    ],
    isDemoData: true
  },
  {
    id: 'rajasthan',
    name: 'Rajasthan',
    type: 'STATE',
    code: 'RJ',
    capital: 'Jaipur',
    region: 'North India',
    latitude: 27.0238,
    longitude: 74.2179,
    primaryRisk: 'Heatwave',
    secondaryRisk: 'Drought',
    riskScore: 83,
    districts: [
      'Barmer', 'Jaisalmer', 'Bikaner', 'Jodhpur', 'Churu',
      'Jaipur', 'Kota', 'Udaipur', 'Ajmer', 'Alwar',
      'Sikar', 'Nagaur', 'Pali', 'Bhilwara', 'Sri Ganganagar'
    ],
    isDemoData: true
  },
  {
    id: 'sikkim',
    name: 'Sikkim',
    type: 'STATE',
    code: 'SK',
    capital: 'Gangtok',
    region: 'Northeast India',
    latitude: 27.5330,
    longitude: 88.5122,
    primaryRisk: 'Landslide',
    secondaryRisk: 'Earthquake',
    riskScore: 85,
    districts: [
      'East Sikkim (Gangtok)', 'West Sikkim (Geyzing)', 'North Sikkim (Mangan)',
      'South Sikkim (Namchi)', 'Pakyong', 'Soreng'
    ],
    isDemoData: true
  },
  {
    id: 'tamil-nadu',
    name: 'Tamil Nadu',
    type: 'STATE',
    code: 'TN',
    capital: 'Chennai',
    region: 'South India',
    latitude: 11.1271,
    longitude: 78.6569,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Flood',
    riskScore: 75,
    districts: [
      'Chennai', 'Cuddalore', 'Nagapattinam', 'Kanchipuram', 'Thiruvallur',
      'Tirunelveli', 'Kanyakumari', 'Coimbatore', 'Madurai', 'Tiruchirappalli',
      'Salem', 'Thanjavur', 'Ramanathapuram', 'Vellore', 'Dindigul'
    ],
    isDemoData: true
  },
  {
    id: 'telangana',
    name: 'Telangana',
    type: 'STATE',
    code: 'TS',
    capital: 'Hyderabad',
    region: 'South India',
    latitude: 18.1124,
    longitude: 79.0193,
    primaryRisk: 'Heatwave',
    secondaryRisk: 'Flood',
    riskScore: 60,
    districts: [
      'Hyderabad', 'Ranga Reddy', 'Medchal-Malkajgiri', 'Warangal', 'Khammam',
      'Karimnagar', 'Nizamabad', 'Mahbubnagar', 'Nalgonda', 'Adilabad',
      'Bhadradri Kothagudem', 'Siddipet', 'Mancherial', 'Kamareddy'
    ],
    isDemoData: true
  },
  {
    id: 'tripura',
    name: 'Tripura',
    type: 'STATE',
    code: 'TR',
    capital: 'Agartala',
    region: 'Northeast India',
    latitude: 23.9408,
    longitude: 91.9882,
    primaryRisk: 'Flood',
    secondaryRisk: 'Earthquake',
    riskScore: 69,
    districts: [
      'West Tripura (Agartala)', 'South Tripura', 'Gomati (Udaipur)', 'Dhalai (Ambassa)',
      'North Tripura (Dharmanagar)', 'Unakoti (Kailashahar)', 'Khowai', 'Sepahijala'
    ],
    isDemoData: true
  },
  {
    id: 'uttar-pradesh',
    name: 'Uttar Pradesh',
    type: 'STATE',
    code: 'UP',
    capital: 'Lucknow',
    region: 'North India',
    latitude: 26.8467,
    longitude: 80.9462,
    primaryRisk: 'Flood',
    secondaryRisk: 'Heatwave',
    riskScore: 73,
    districts: [
      'Lucknow', 'Kanpur', 'Varanasi', 'Prayagraj (Allahabad)', 'Gorakhpur',
      'Agra', 'Meerut', 'Ghaziabad', 'Noida (Gautam Buddha Nagar)', 'Bareilly',
      'Aligarh', 'Moradabad', 'Ayodhya', 'Jhansi', 'Banda', 'Lakhimpur Kheri'
    ],
    isDemoData: true
  },
  {
    id: 'uttarakhand',
    name: 'Uttarakhand',
    type: 'STATE',
    code: 'UK',
    capital: 'Dehradun',
    region: 'North India',
    latitude: 30.0668,
    longitude: 79.0193,
    primaryRisk: 'Landslide',
    secondaryRisk: 'Flood',
    riskScore: 89,
    districts: [
      'Chamoli', 'Rudraprayag', 'Uttarkashi', 'Dehradun', 'Tehri Garhwal',
      'Pithoragarh', 'Nainital', 'Haridwar', 'Pauri Garhwal', 'Almora',
      'Bageshwar', 'Champawat', 'Udham Singh Nagar'
    ],
    isDemoData: true
  },
  {
    id: 'west-bengal',
    name: 'West Bengal',
    type: 'STATE',
    code: 'WB',
    capital: 'Kolkata',
    region: 'East India',
    latitude: 22.9868,
    longitude: 87.8550,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Flood',
    riskScore: 77,
    districts: [
      'Kolkata', 'South 24 Parganas (Sundarbans)', 'North 24 Parganas', 'Howrah',
      'Purba Medinipur', 'Paschim Medinipur', 'Darjeeling', 'Jalpaiguri',
      'Kalimpong', 'Alipurduar', 'Murshidabad', 'Nadia', 'Malda', 'Bankura'
    ],
    isDemoData: true
  }
];

export const ALL_INDIAN_UNION_TERRITORIES: IndiaLocation[] = [
  {
    id: 'andaman-nicobar',
    name: 'Andaman and Nicobar Islands',
    type: 'UNION_TERRITORY',
    code: 'AN',
    capital: 'Port Blair',
    region: 'Islands',
    latitude: 11.7401,
    longitude: 92.6586,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Earthquake',
    riskScore: 76,
    districts: [
      'South Andaman (Port Blair)', 'North and Middle Andaman (Mayabunder)', 'Nicobar (Car Nicobar)'
    ],
    isDemoData: true
  },
  {
    id: 'chandigarh',
    name: 'Chandigarh',
    type: 'UNION_TERRITORY',
    code: 'CH',
    capital: 'Chandigarh',
    region: 'North India',
    latitude: 30.7333,
    longitude: 76.7794,
    primaryRisk: 'Heatwave',
    secondaryRisk: 'Flood',
    riskScore: 42,
    districts: [
      'Chandigarh (Urban)', 'Sector 1-17 (Central)', 'Industrial Area', 'Manimajra', 'Sukhna Lake Basin'
    ],
    isDemoData: true
  },
  {
    id: 'dadra-nagar-haveli',
    name: 'Dadra and Nagar Haveli',
    type: 'UNION_TERRITORY',
    code: 'DNH',
    capital: 'Silvassa',
    region: 'West India',
    latitude: 20.2763,
    longitude: 73.0083,
    primaryRisk: 'Flood',
    secondaryRisk: 'Cyclone',
    riskScore: 54,
    districts: [
      'Silvassa', 'Amli', 'Khanvel', 'Naroli', 'Dadra Enclave'
    ],
    isDemoData: true
  },
  {
    id: 'daman-diu',
    name: 'Daman and Diu',
    type: 'UNION_TERRITORY',
    code: 'DD',
    capital: 'Daman',
    region: 'West India',
    latitude: 20.4283,
    longitude: 72.8397,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Flood',
    riskScore: 63,
    districts: [
      'Daman (Moti Daman & Nani Daman)', 'Diu (Ghoghla & Fort)'
    ],
    isDemoData: true
  },
  {
    id: 'delhi',
    name: 'Delhi',
    type: 'UNION_TERRITORY',
    code: 'DL',
    capital: 'New Delhi',
    region: 'North India',
    latitude: 28.7041,
    longitude: 77.1025,
    primaryRisk: 'Flood',
    secondaryRisk: 'Heatwave',
    riskScore: 67,
    districts: [
      'East Delhi (Yamuna Basin)', 'North East Delhi', 'South East Delhi',
      'Central Delhi', 'New Delhi', 'North Delhi', 'North West Delhi',
      'West Delhi', 'South Delhi', 'South West Delhi', 'Shahdara'
    ],
    isDemoData: true
  },
  {
    id: 'jammu-kashmir',
    name: 'Jammu and Kashmir',
    type: 'UNION_TERRITORY',
    code: 'JK',
    capital: 'Srinagar / Jammu',
    region: 'North India',
    latitude: 33.7782,
    longitude: 76.5762,
    primaryRisk: 'Flood',
    secondaryRisk: 'Earthquake',
    riskScore: 81,
    districts: [
      'Srinagar (Jhelum Basin)', 'Anantnag', 'Baramulla', 'Jammu (Tawi Basin)',
      'Doda', 'Poonch', 'Kupwara', 'Budgam', 'Pulwama', 'Kishtwar', 'Kathua', 'Udhampur'
    ],
    isDemoData: true
  },
  {
    id: 'ladakh',
    name: 'Ladakh',
    type: 'UNION_TERRITORY',
    code: 'LA',
    capital: 'Leh',
    region: 'North India',
    latitude: 34.1526,
    longitude: 77.5771,
    primaryRisk: 'Landslide',
    secondaryRisk: 'Earthquake',
    riskScore: 77,
    districts: [
      'Leh (Indus Valley)', 'Kargil (Suru Basin)', 'Nubra Valley', 'Zanskar', 'Changthang'
    ],
    isDemoData: true
  },
  {
    id: 'lakshadweep',
    name: 'Lakshadweep',
    type: 'UNION_TERRITORY',
    code: 'LD',
    capital: 'Kavaratti',
    region: 'Islands',
    latitude: 10.5667,
    longitude: 72.6417,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Flood',
    riskScore: 70,
    districts: [
      'Kavaratti Island', 'Agatti Island', 'Amini Island', 'Andrott Island',
      'Minicoy Island', 'Kalpeni Island', 'Kadmat Island'
    ],
    isDemoData: true
  },
  {
    id: 'puducherry',
    name: 'Puducherry',
    type: 'UNION_TERRITORY',
    code: 'PY',
    capital: 'Puducherry',
    region: 'South India',
    latitude: 11.9416,
    longitude: 79.8083,
    primaryRisk: 'Cyclone',
    secondaryRisk: 'Flood',
    riskScore: 66,
    districts: [
      'Puducherry (Coromandel Coast)', 'Karaikal', 'Mahe (Malabar Coast)', 'Yanam (Godavari Delta)'
    ],
    isDemoData: true
  }
];

/**
 * Combined dataset of exactly 28 States and 9 Union Territories (37 total locations)
 */
export const ALL_INDIAN_LOCATIONS: IndiaLocation[] = [
  ...ALL_INDIAN_STATES,
  ...ALL_INDIAN_UNION_TERRITORIES
];

/**
 * Helper to find location by ID or Name (case-insensitive)
 */
export const findIndiaLocation = (query: string): IndiaLocation | undefined => {
  const q = query.toLowerCase().trim();
  return ALL_INDIAN_LOCATIONS.find(
    (l) =>
      l.id.toLowerCase() === q ||
      l.name.toLowerCase() === q ||
      l.code.toLowerCase() === q ||
      (q.includes('dadra') && (l.id === 'dadra-nagar-haveli' || l.id === 'daman-diu')) ||
      (q.includes('daman') && (l.id === 'daman-diu' || l.id === 'dadra-nagar-haveli'))
  );
};
