class StaminaComponent:
    def __init__(self, max_stamina, drain_rate, recover_rate):
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina
        self.drain_rate = drain_rate  # Quanto gasta por segundo ao correr
        self.recover_rate = recover_rate  # Quanto recupera por segundo em repouso

    def update(self, dt, is_running):
        if is_running:
            self.current_stamina -= self.drain_rate * dt
        else:
            self.current_stamina += self.recover_rate * dt

        self.current_stamina = max(0, min(self.max_stamina, self.current_stamina))