
employers_data = [
    { "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    { "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    { "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    { "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    { "title": "Accountant II", "description": "Manage financial records", "employer_id": 2},
    { "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]

users_data = [
    {"username": "mia", "email": "mia@email.com", "password": "password", "role": "admin" },
    {"username": "gilbert", "email": "gilbert@email.com", "password": "password", "role": "admin" },
    {"username": "willow", "email": "willow@email.com", "password": "password", "role": "admin" }
]

applications_data = [
    {"user_id": 1, "job_id": 1},
    {"user_id": 2, "job_id": 2},
    {"user_id": 2, "job_id": 3},
    {"user_id": 1, "job_id": 4}
]

companies = [
    {
        "id": 1,
        "name": "88 car wash",
        "about": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid veritatis animi numquam! Mollitia facere, excepturi dolor",
        "logo": "https://cdn.worldvectorlogo.com/logos/lorem-lorem.svg",
        "address": "Mandaluyong, Metro Manila, Philippines"
    }
]

vehicle_types = [
    {"name": "sedan"},
    {"name": "hatchback"},
    {"name": "pickup"},
    {"name": "suv"},
    {"name": "van"},
    {"name": "close van"},
    {"name": "caravan"},
    {"name": "motorcycle"}
]

posts = [
    {
        "id": 1,
        "title": "88 car wash",
        "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid veritatis animi numquam! Mollitia facere, excepturi dolore, dicta ullam harum nemo autem ipsam reiciendis, a eligendi qui at maxime nihil ipsum!",
        "rating": 4.5,
        "booking_count": 11,
        "company_id": 1,  # Connect the post to a company using the company_id
        "user_profile_id": 1, 
        "prices": [
            {"vehicle_type": "sedan", "price": 300.00},
            {"vehicle_type": "hatchback", "price": 300.00},
            {"vehicle_type": "suv", "price": 300.00},
            {"vehicle_type": "van", "price": 300.00},
            {"vehicle_type": "close van", "price": 300.00},
            {"vehicle_type": "caravan", "price": 300.00},
            {"vehicle_type": "motorcycle", "price": 300.00},
        ],
        "images": [
            {"image_url": "https://fastly.picsum.photos/id/334/536/354.jpg?hmac=Fqr45rgKed7wdrBcTfry45TVJTcjO1smvFBhSRsaeqY"},
            {"image_url": "https://fastly.picsum.photos/id/334/536/354.jpg?hmac=Fqr45rgKed7wdrBcTfry45TVJTcjO1smvFBhSRsaeqY"},
            {"image_url": "https://fastly.picsum.photos/id/334/536/354.jpg?hmac=Fqr45rgKed7wdrBcTfry45TVJTcjO1smvFBhSRsaeqY"},
            {"image_url": "https://fastly.picsum.photos/id/334/536/354.jpg?hmac=Fqr45rgKed7wdrBcTfry45TVJTcjO1smvFBhSRsaeqY"},
            {"image_url": "https://fastly.picsum.photos/id/334/536/354.jpg?hmac=Fqr45rgKed7wdrBcTfry45TVJTcjO1smvFBhSRsaeqY"},
        ],
        "addons": [
            {
                "name": "Sealer Hand Wax",
                "description": "Lorem ipsum",
                "price": 300.00
            },
        ],
    }
]

reviews = [
    {
        "username": "Ronnel Anthony",
        "message": "We had a very awesome stay in this place. The unit is complete with everything you need even first aid kit. The location is perfect, the room is equipped and clean. The host is very…",
        "post_id": 1,  # Connect the review to a post using the post_id
    }
]

bookings = [
    {
        "booking_id": 1,
        "post_id": 1,
        "user_profile_id": 1,  # Connect the booking to a user profile using the user_profile_id
        "user_name": "John Doe",
        "booking_date": "2023-11-15",
        "vehicle_type": "sedan",
        "price": 300.00,
        "status": "confirmed",
    },
    {
        "booking_id": 2,
        "post_id": 1,
        "user_profile_id": 2,  # Connect the booking to a different user profile
        "user_name": "Alice Smith",
        "booking_date": "2023-11-16",
        "vehicle_type": "suv",
        "price": 300.00,
        "status": "confirmed",
    },
]