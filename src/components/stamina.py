class StaminaComponent:
    def __init__(self, max_stamina=100, drain_rate=25, recover_rate=15):
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina
        self.drain_rate = drain_rate  # Quantidade consumida por segundo ao correr
        self.recover_rate = recover_rate  # Quantidade recuperada por segundo em repouso
        self.is_exhausted = False  # Novo estado de exaustão

    def update(self, dt, is_running):
        if is_running:
            self.current_stamina -= self.drain_rate * dt
            if self.current_stamina <= 0:
                self.current_stamina = 0
                self.is_exhausted = True
        else:
            self.current_stamina += self.recover_rate * dt
            if self.current_stamina >= self.max_stamina:
                self.current_stamina = self.max_stamina
                self.is_exhausted = False

        self.current_stamina = max(0, min(self.max_stamina, self.current_stamina))