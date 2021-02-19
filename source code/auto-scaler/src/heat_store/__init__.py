class HeatStore:
    def __init__(self):
        self._store = {}

    def _calculate_heat(self, heat: int, utilization: int,
                        min_utilization: int, max_utilization: int):
        if utilization >= max_utilization:
            if heat < 0:
                heat = 0
            heat = heat + 1
        elif utilization <= min_utilization:
            if heat > 0:
                heat = 0
            heat = heat - 1
        else:
            if heat > 0:
                heat = heat - 1
            elif heat < 0:
                heat = heat + 1

        return heat

    def update_heat(self, metric: str, thresholds, utilization: int):
        heat = self._calculate_heat(self.get_heat(metric), utilization,
                                    thresholds.min, thresholds.max)
        self._store[metric] = heat

    def get_heat(self, metric: str):
        return self._store.get(metric, 0)

    def reset_heat(self, metric: str):
        self._store[metric] = 0
