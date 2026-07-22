from the_disaster_response_agent.tools.resource_tool import find_nearby_resources

# Test with Islamabad coordinates
result = find_nearby_resources(latitude=33.6844, longitude=73.0479, radius=5000)
print("hospitals:", result["hospitals"][:3])
print("shelters:", result["shelters"][:3])
print("note:", result["note"])
