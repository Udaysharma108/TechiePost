# bharatfeed/constants.py

# Comprehensive geographic footprint tracking tech hubs across all tiers
INDIAN_CITIES = [
    'bengaluru', 'bangalore', 'pune', 'mumbai', 'delhi', 'noida', 'gurugram', 'gurgaon',
    'hyderabad', 'chennai', 'kolkata', 'ahmedabad', 'thiruvananthapuram', 'trivandrum',
    'kochi', 'coimbatore', 'indore', 'jaipur', 'bhubaneswar', 'chandigarh', 'nagpur',
    'lucknow', 'kanpur', 'mysuru', 'mysore', 'mangaluru', 'mangalore', 'visakhapatnam', 'vizag'
]

# Heavyweight Tech Giants, IT Exporters, Deep-Tech Pioneers, and Scale-up Unicorns
INDIAN_COMPANIES = [
    # IT Service & Systems Giants
    'tcs', 'tata consultancy services', 'infosys', 'wipro', 'hcl', 'tech mahindra', 
    'ltimindtree', 'cognizant', 'mphasis', 'persistent systems', 'lti', 'mindtree',
    
    # Telecommunications & Network Infrastructures
    'jio', 'reliance jio', 'reliance industries', 'airtel', 'bharti airtel', 'vodafone idea',
    
    # Tech Unicorns & Consumer Tech Platforms
    'ola electric', 'ola cabs', 'zomato', 'swiggy', 'paytm', 'flipkart', 'phonepe', 
    'razorpay', 'zerodha', 'groww', 'meesho', 'zepto', 'blinkit', 'inmobi', 'postman', 
    'hasura', 'browserstack', 'cred', 'nykaa', 'policybazaar', 'delhivery', 'byjus',
    'unacademy', 'urban company', 'lenskart', 'bigbasket', 'mapmyindia', 'fractal analytics',
    
    # Emerging AI, SaaS, & Semiconductor Startups
    'krutrim', 'sarvam ai', 'ola krutrim', 'kaiber', 'zoho', 'freshworks', 'chargebee', 
    'capillary technologies', 'druva', 'cohesity', 'applied materials india'
]

# Elite Academic Institutions, Advanced Computing Hubs, & Aerospace Centers
INDIAN_INSTITUTES = [
    # Indian Institutes of Technology (All Primary Tech Campuses)
    'iit', 'iit bombay', 'iit madras', 'iit delhi', 'iit kharagpur', 'iit kanpur', 
    'iit roorkee', 'iit guwahati', 'iit hyderabad', 'iit bhu', 'iit indore', 'iit ropar',
    
    # National & International Research Frontiers
    'iisc', 'indian institute of science', 'tifr', 'tata institute of fundamental research',
    'barc', 'bhabha atomic research centre', 'bits pilani', 'nit', 'iiit', 'iiit hyderabad',
    'iiit bangalore', 'nasscom', 'iim', 'vjti', 'coep', 'ict mumbai'
]

# Space, Defense, Autonomous Hardware, and Advanced Research Laboratories
INDIAN_GOVT_TECH_AGENCIES = [
    'isro', 'indian space research organisation', 'vssc', 'sac', 'ursc', 'antrix', 'nsl',
    'drdo', 'defence research and development organisation', 'ada', 'hal', 'bel',
    'cdac', 'centre for development of advanced computing', 'nic', 'national informatics centre',
    'csir', 'tifac', 'semiconductor laboratory', 'scl mohali'
]

# Digital Public Infrastructure (DPI), Gov-Tech Platforms, and National Initiatives
INDIAN_DPI_AND_GOVT_INITIATIVES = [
    # Digital Public Infrastructure (Ecosystem Infrastructure)
    'meity', 'ministry of electronics and information technology', 'uidai', 'aadhaar', 
    'upi', 'unified payments interface', 'npci', 'national payments corporation of india', 
    'indiastack', 'india stack', 'bhashini', 'ai4bharat', 'ndhm', 'abdm', 'onplay',
    'ondc', 'open network for digital commerce', 'gem portal', 'digilocker', 'cowin',
    
    # Macro Frameworks & Structural Incentives
    'digital india', 'make in india', 'startup india', 'atal innovation mission', 'aim',
    'pli scheme', 'india semiconductor mission', 'ism', 'param supercomputing'
]

# Key Policymakers, Technology Ministers, and National Digital Architects
INDIAN_TECH_LEADERS = [
    'narendra modi', 'ashwini vaishnaw', 'rajeev chandrasekhar', 's somanath',
    'nandan nilekani', 'amitabh kant', 'k vijayraghavan', 'ajay kumar sood'
]

# Institutional High-Conviction VCs Backing Indian Core Tech Founder Networks
INDIAN_VC_FIRMS = [
    'sequoia india', 'peak xv', 'peak xv partners', 'elevation capital', 'matrix partners india',
    'nexus venture partners', 'kalaari capital', 'chiratae ventures', ' Blume ventures', 
    'accel india', 'lightspeed india', 'inflection point ventures', 'india quotient'
]

# Master Data Aggregation Matrix Compiled Into a High-Speed Lookup Set
BHARAT_TECH_MATRIX = set(
    INDIAN_CITIES + 
    INDIAN_COMPANIES + 
    INDIAN_INSTITUTES + 
    INDIAN_GOVT_TECH_AGENCIES + 
    INDIAN_DPI_AND_GOVT_INITIATIVES + 
    INDIAN_TECH_LEADERS + 
    INDIAN_VC_FIRMS
)