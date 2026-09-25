class TemperatureAgent:
    def __init__(self, desired_temperature):
        self.desired_temperature = desired_temperature
        self.heater_on = False
        self.ac_on = False

    def act(self, current_temperature):
        actions = []

        if current_temperature < self.desired_temperature:
            if not self.heater_on:
                self.heater_on = True
                actions.append("Turning heater ON")
        else:
            if self.heater_on:
                self.heater_on = False
                actions.append("Turning heater OFF")

        if current_temperature > 26:
            if not self.ac_on:
                self.ac_on = True
                actions.append("Turning AC ON")
        else:
            if self.ac_on:
                self.ac_on = False
                actions.append("Turning AC OFF")

        if not actions:
            return "No change"

        return " | ".join(actions)


agent = TemperatureAgent(desired_temperature=22)

temperatures = [18, 20, 23, 27, 27, 25, 19, 19]

for temperature in temperatures:
    print(f"{temperature}°C -> {agent.act(temperature)}")