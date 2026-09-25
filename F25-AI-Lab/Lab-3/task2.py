class ModelBasedReflexAgent:
    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.heater_on = False

    def act(self, current_temperature):
        should_be_on = current_temperature < self.desired_temperature

        if should_be_on and not self.heater_on:
            self.heater_on = True
            return "Turning heater ON"
        elif not should_be_on and self.heater_on:
            self.heater_on = False
            return "Turning heater OFF"
        else:
            return "No change (heater already in correct state)"


agent = ModelBasedReflexAgent(desired_temperature=22)

temperatures = [18, 22, 25, 25, 19]

for temperature in temperatures:
    print(f"{temperature}°C -> {agent.act(temperature)}")