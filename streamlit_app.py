import streamlit as st
import google.generativeai as genai

st.title("🗺️ AI Travel Planner & Guide")

# Initialize session state for storing chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize with an empty list

# Input field for API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Authenticate with the API service
if gemini_api_key:
    try:
        genai.configure(api_key=gemini_api_key)
        st.success("Gemini API Key validated successfully!")
    except Exception as e:
        st.error(f"Gemini API Key validation failed: {e}")

# Predefined travel data
destinations = {
    "Buckingham Palace": "The official residence of the British monarch, offering guided tours and a glimpse into royal history.",
    "Tower of London": "A historic castle and former prison, showcasing the Crown Jewels and a collection of ancient armor.",
    "The London Eye": "A giant Ferris wheel offering panoramic city views from 135 meters above the ground."
}

restaurants = {
    "The Ivy": "A renowned restaurant in Covent Garden, known for its celebrity clientele and classic British cuisine.",
    "Hawksmoor": "A popular steakhouse with several locations in London, offering a wide selection of cuts and an extensive wine list.",
    "Gordon Ramsay's Maze": "A Michelin-starred restaurant offering contemporary European cuisine in the Mayfair neighborhood."
}

hotels = {
    "The Savoy": "A luxurious hotel in the Strand, with elegant rooms, a renowned tea service, and a popular riverside restaurant.",
    "The Lanesborough": "A grand hotel in Knightsbridge, offering spacious suites, a state-of-the-art spa, and a Michelin-starred restaurant.",
    "The Beaumont": "A stylish hotel in Mayfair, featuring Art Deco interiors, a cozy bar, and a rooftop terrace with city views."
}

transportation = {
    "Public Transport": "London has an extensive public transportation system, including the Underground (metro), buses, and trains. It's a convenient and affordable way to get around the city.",
    "Car Rental": "Renting a car provides flexibility and convenience, especially if you plan to explore outside of London. However, parking can be expensive in central areas.",
    "Walking": "London is a walkable city, with many attractions located within walking distance of each other. It's a great way to soak up the atmosphere and explore at your own pace."
}

activities = {
    "Thames River Cruise": "Enjoy a scenic boat cruise along the Thames River, passing by iconic landmarks such as the Tower Bridge, the London Eye, and the Houses of Parliament. A perfect way to see the city from a unique perspective.",
    "West End Theatre Show": "Experience world-class theatre in London's West End. From musicals like 'The Phantom of the Opera' and 'Hamilton' to classic plays, there's something for everyone.",
    "Borough Market": "Visit one of London's oldest and most renowned food markets. Sample a variety of local and international delicacies, and enjoy the vibrant atmosphere.",
    "Harry Potter Studio Tour": "Explore the magical world of Harry Potter at Warner Bros. Studio. See the original sets, costumes, and props from the films, and learn about the filmmaking process.",
    "Sky Garden": "Take in panoramic views of London from the Sky Garden, located at the top of the 'Walkie Talkie' building. It's a free public space with lush greenery and stunning vistas."
}

# Function to generate travel suggestions based on user input
def generate_travel_suggestions(user_input):
    response = ""
    # Check if user input matches any predefined destinations
    for destination, description in destinations.items():
        if destination.lower() in user_input.lower():
            response += f"**{destination}**: {description}\n\n"

    # Check if user input matches any predefined restaurants
    for restaurant, description in restaurants.items():
        if restaurant.lower() in user_input.lower():
            response += f"**{restaurant}**: {description}\n\n"

    # Check if user input matches any predefined hotels
    for hotel, description in hotels.items():
        if hotel.lower() in user_input.lower():
            response += f"**{hotel}**: {description}\n\n"

    # Check if user input matches any predefined transportation options
    for transport, description in transportation.items():
        if transport.lower() in user_input.lower():
            response += f"**{transport}**: {description}\n\n"

    # Check if user input matches any predefined activities
    for activity, description in activities.items():
        if activity.lower() in user_input.lower():
            response += f"**{activity}**: {description}\n\n"

    # If no specific match found, return general travel prompt
    if response == "":
        if gemini_api_key:
            try:
                model = genai.GenerativeModel("gemini-pro")
                travel_prompt = f"""
                You are a travel planning assistant. Provide recommendations for destinations, famous restaurants, popular hotels, and transportation options based on the user's query.
                User query: {user_input}
                """
                response = model.generate_content(travel_prompt).text
            except Exception as e:
                response = f"Error generating response: {e}"
        else:
            response = "API Key is not set."
    return response

# Capture user input using st.chat_input
user_input = st.chat_input("Type your travel-related query here...")

# Generate AI response and update chat history
if user_input:
    # Append user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Generate travel suggestions and add to chat history
    bot_response = generate_travel_suggestions(user_input)
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

# Display chat messages using st.chat_message
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])