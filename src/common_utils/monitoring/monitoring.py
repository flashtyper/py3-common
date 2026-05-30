from typing import Union


class Monitoring:
    def __init__(self):
        self.states = {'0': 'OK', '1': 'WARNING', '2': 'CRITICAL', '3': 'UNKNOWN'}
        self.state = 0
        self.perf_data = []
        self.output = []

    def exit_plugin(self):
        # Prints the outputs, perfata and exits accordingly its state
        if self.perf_data:
            print(self.states[str(self.state)] + ' - ' + '\n'.join(self.output) + ' | ' + ' '.join(self.perf_data))
        else:
            print(self.states[str(self.state)] + ' - ' + '\n'.join(self.output))
        exit(self.state)

    def escalate_to(self, new_state: Union[str, int]) -> bool:
        # Escalates internal state if new_state > internal state
        if isinstance(new_state, str):
            new_state = self.states[new_state]
        if new_state == self.state:
            return False
        elif new_state > self.state:
            self.state = new_state
            return True
        return False

    def add_perfdata(self, label: str, value: Union[int, float], uom: str = '') -> None:
        # Adds a perfdata to the plugin output
        self.perf_data.append(f'{label}={value}{uom}')

    def check_threshold(self, value: Union[int, float], low_warn, high_warn, low_crit, high_crit) -> bool:
        # Checks if a given value lays between thresholds and escalates the internal state
        # Returns False, if no threshold is crossed. True otherwise.
        if value <= low_crit or value >= high_crit:
            self.escalate_to(2)
            return True
        elif (low_warn >= value > low_crit) or (high_warn <= value < high_crit):
            self.escalate_to(1)
            return True
        return False

    def build_message(self, label: str, message: str):
        # Adds a label with message to the plugin output
        self.output.append(f'{label}: {message}')

    def build_message_and_set_state(self, new_state: Union[str, int], label: str, message: str):
        # Adds a label with message to the plugin output and sets
        # the current state to `new_state`
        self.output.append(f'{label}: {message}')
        if isinstance(new_state, str):
            new_state_number = self.states[new_state]
        else:
            new_state_number = new_state
       self.state = new_state_number

