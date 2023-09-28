from django.core.management.base import BaseCommand
from ecommerce_app.models import State, City

class Command(BaseCommand):
    help = 'Populate states and cities in the database'

    def handle(self, *args, **options):
        # Clear existing states and cities (optional)
        State.objects.all().delete()
        City.objects.all().delete()
        
        # Define the states and their respective cities
        
        state_cities = {
            'Andaman and Nicobar Islands': ['Nicobar', 'North and Middle Andaman', 'South Andaman'],
            
            'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari',
                               'Guntur', 'Krishna', 'Kurnool', 'Nellore', 
                               'Prakasam', 'Srikakulam', 'Visakhapatnam', 
                               'Vizianagaram', 'West Godavari', 'YSR Kadapa'],
            
            'Arunachal Pradesh': ['Tawang', 'West Kameng', 'East Kameng', 'Papum Pare',
                                  'Kurung Kumey', 'Kra Daadi', 'Lower Subansiri', 'Upper Subansiri',
                                  'West Siang', 'East Siang', 'Siang', 'Upper Siang', 'Lower Siang',
                                  'Lower Dibang Valley', 'Dibang Valley', 'Anjaw', 'Lohit', 'Namsai',
                                  'Changlang', 'Tirap', 'Longding', 'Pakke Kessang', 'Kamle', 'Lepa Rada',
                                  'Papum Poma', 'Kolaktang', 'Tirbin', 'Basa', 'Chayang Tajo', 'Lada'],
            
            'Assam': ['Baksa', 'Barpeta', 'Biswanath', 'Bongaigaon', 'Cachar', 'Charaideo', 'Chirang',
                      'Darrang', 'Dhemaji', 'Dhubri', 'Dibrugarh', 'Goalpara', 'Golaghat', 'Hailakandi', 
                      'Hojai', 'Jorhat', 'Kamrup', 'Kamrup Metropolitan', 'Karbi Anglong', 'Karimganj', 
                      'Kokrajhar', 'Lakhimpur', 'Majuli', 'Morigaon', 'Nagaon', 'Nalbari', 'Dima Hasao',
                      'Sivasagar', 'Sonitpur', 'South Salmara-Mankachar', 'Tinsukia', 'Udalguri', 
                      'West Karbi Anglong'],
            
            'Bihar': ['Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 
                      'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran',
                      'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar',
                      'Khagaria', 'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 
                      'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada', 'Patna', 'Purnia', 
                      'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar',
                      'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'West Champaran'],
            
            'Chandigarh': ['Chandigarh'],
            
            'Chhattisgarh': ['Balod', 'Baloda Bazar', 'Balrampur', 'Bastar', 'Bemetara', 
                             'Bijapur', 'Bilaspur', 'Dantewada', 'Dhamtari', 'Durg', 'Gariaband', 
                             'Gaurela-Pendra-Marwahi', 'Janjgir-Champa', 'Jashpur', 'Kanker', 
                             'Kondagaon', 'Korba', 'Koriya', 'Mahasamund', 'Mungeli', 'Narayanpur', 
                             'Raigarh', 'Raipur', 'Rajnandgaon', 'Sukma', 'Surajpur', 'Surguja'],
            
            'Dadra and Nagar Haveli': ['Silvassa'],
            'Daman and Diu': ['Daman', 'Diu'],
            'Delhi': ['Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 'North East Delhi', 'North West Delhi', 'Shahdara', 'South Delhi', 'South East Delhi', 'South West Delhi', 'West Delhi']
,
            'Goa': ['North Goa', 'South Goa']
,
            
            'Gujarat': ['Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar',
                        'Botad','Chhota Udaipur', 'Dahod', 'Dang', 'Devbhoomi Dwarka','Gandhinagar',
                        'Gir Somnath', 'Jamnagar', 'Junagadh','Kutch', 'Kheda', 'Mahisagar', 'Mehsana', 'Morbi',
                        'Narmada','Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha',
                        'Surat', 'Surendranagar', 'Tapi', 'Vadodara', 'Valsad'],
            
            'Haryana': ['Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Guraon/Gurugram', 
                        'Hisar', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh',
                        'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat',
                        'Yamunanagar'],
            
            'Himachal Pradesh': ['Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu',
                                 'Lahaul and Spiti', 'Mandi', 'Shimla', 'Sirmaur', 'Solan', 'Una']
,
            'Jammu and Kashmir': ['Anantnag', 'Bandipora', 'Baramulla', 'Budgam', 'Doda', 'Ganderbal', 
                                  'Jammu', 'Kathua', 'Kishtwar', 'Kulgam', 'Kupwara', 'Poonch', 'Pulwama',
                                  'Rajouri', 'Ramban', 'Reasi', 'Samba', 'Shopian', 'Srinagar', 'Udhampur'],
            
            'Jharkhand': ['Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum',
                          'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Jamtara', 'Khunti',
                          'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 
                          'Sahibganj', 'Seraikela Kharsawan', 'Simdega', 'West Singhbhum']
,
            'Karnataka': ['Bagalkot', 'Ballari', 'Belagavi', 'Bengaluru Rural', 'Bengaluru Urban',
                          'Bidar', 'Chamarajanagar', 'Chikkaballapur', 'Chikkamagaluru', 'Chitradurga', 
                          'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 
                          'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Raichur', 
                          'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura', 
                          'Yadgir']
,
            'Kerala':['Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 
                      'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram',
                      'Thrissur', 'Wayanad']
,
            'Lakshadweep': ['Kavaratti'],
            
            'Madhya Pradesh': ['Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani',
                               'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh',
                               'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad',
                               'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 'Khargone', 'Mandla', 
                               'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Panna', 'Raisen', 'Rajgarh',
                               'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur',
                               'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria',
                               'Vidisha']
,
            'Maharashtra':['Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana',
                           'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 
                           'Kolhapur', 'Latur', 'Mumbai City', 'Mumbai Suburban', 'Nagpur', 'Nanded', 
                           'Nandurbar', 'Nashik', 'Osmanabad', 'Palghar', 'Parbhani', 'Pune', 'Raigad',
                           'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 
                           'Washim', 'Yavatmal'],
            
            'Manipur': ['Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 'Jiribam',
                        'Kakching', 'Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 'Senapati', 'Tamenglong',
                        'Tengnoupal', 'Thoubal', 'Ukhrul'],
            
            'Meghalaya': ['East Garo Hills', 'East Jaintia Hills', 'East Khasi Hills', 'North Garo Hills', 
                          'Ri-Bhoi', 'South Garo Hills', 'South West Garo Hills', 'South West Khasi Hills',
                          'West Garo Hills', 'West Jaintia Hills', 'West Khasi Hills'],
            
            'Mizoram': ['Aizawl', 'Champhai', 'Hnahthial', 'Khawzawl', 'Kolasib', 'Lawngtlai', 'Lunglei',
                        'Mamit', 'Saiha', 'Saitual', 'Serchhip'],
            
            'Nagaland': ['Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Noklak', 'Peren',
                         'Phek', 'Tuensang', 'Wokha', 'Zunheboto'],
            
            'Odisha': ['Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh',
                       'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi',
                       'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj',
                       'Nabarangpur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur',
                       'Sundargarh'],
            
            'Puducherry': ['Puducherry'],
            
            'Punjab': ['Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur',
                       'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 
                       'Muktsar', 'Nawanshahr', 'Pathankot', 'Patiala', 'Rupnagar', 'Sahibzada Ajit Singh Nagar',
                       'Sangrur', 'Shahid Bhagat Singh Nagar', 'Sri Muktsar Sahib', 'Tarn Taran'],
            
            'Rajasthan': ['Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer', 'Bharatpur', 'Bhilwara', 'Bikaner',
                          'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 'Hanumangarh',
                          'Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Karauli',
                          'Kota', 'Nagaur', 'Pali', 'Pratapgarh', 'Rajsamand', 'Sawai Madhopur', 'Sikar',
                          'Sirohi', 'Sri Ganganagar', 'Tonk', 'Udaipur'],
            
            'Sikkim': ['East Sikkim', 'North Sikkim', 'South Sikkim', 'West Sikkim'],
            
            'Tamil Nadu': ['Ariyalur', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul',
                           'Erode', 'Kanchipuram', 'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai',
                           'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram',
                           'Salem', 'Sivaganga', 'Thanjavur', 'Theni', 'Thoothukudi', 'Tiruchirappalli', 
                           'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur',
                           'Vellore', 'Viluppuram', 'Virudhunagar'],
            
            'Telangana': ['Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon', 
                          'Jayashankar Bhupalapally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam',
                          'Komaram Bheem', 'Mahabubabad', 'Mahabubnagar', 'Mancherial', 'Medak',
                          'Medchal-Malkajgiri', 'Mulugu', 'Nagarkurnool', 'Nalgonda', 'Nirmal', 'Nizamabad', 
                          'Peddapalli', 'Rajanna Sircilla', 'Ranga Reddy', 'Sangareddy', 'Siddipet', 'Suryapet',
                          'Vikarabad', 'Wanaparthy', 'Warangal Rural', 'Warangal Urban', 'Yadadri Bhuvanagiri'],
            
            'Tripura': ['Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sepahijala', 'South Tripura', 'Unakoti',
                        'West Tripura'],
            
            'Uttar Pradesh': [
                'Agra', 'Aligarh', 'Allahabad', 'Ambedkar Nagar', 'Amethi','Amroha', 'Auraiya', 'Azamgarh',
                'Baghpat', 'Bahraich', 'Ballia','Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi',
                'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot','Deoria', 'Etah', 'Etawah',
                'Faizabad', 'Farrukhabad', 'Fatehpur','Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur',
                'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras','Jalaun', 'Jaunpur', 'Jhansi',
                'Kannauj', 'Kanpur Dehat','Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Kheri', 'Kushinagar',
                'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri','Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad',
                'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Raebareli','Rampur', 'Saharanpur', 'Sambhal', 
                'Sant Kabir Nagar','Shahjahanpur', 'Shamli', 'Shravasti', 'Siddharthnagar',
                'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi'],
            
            'Uttarakhand': ['Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 'Nainital', 
                            'Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 'Udham Singh Nagar', 
                            'Uttarkashi'],
            
            }


        # Populate the states and cities in the database
        for state_name, cities in state_cities.items():
            state = State.objects.create(name=state_name)
            for city_name in cities:
                City.objects.create(name=city_name, state=state)

        self.stdout.write(self.style.SUCCESS('States and cities populated successfully.'))
