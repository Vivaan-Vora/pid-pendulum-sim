    def close(self) -> None:
        if self.enabled and plt is not None:
            plt.ioff()
            plt.close(self.fig)
