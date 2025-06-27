from booking_agent import AgentState, booking_graph

# Simulate a test input for the booking assistant
output = booking_graph.invoke({
    "user_input": "I want to book an appointment for 2pm today"
})

# Print the agent's response
print("🤖 Agent Response:\n", output["response"])
