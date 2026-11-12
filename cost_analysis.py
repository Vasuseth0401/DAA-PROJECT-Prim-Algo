
class CostAnalysis:

    def __init__(self, graph, mst_edges, mst_cost):
        self.graph = graph
        self.mst_edges = mst_edges
        self.mst_cost = mst_cost

        print("[SUCCESS] Cost Analysis initialized!")

    def calculate_total_network_cost(self):

        connections = self.graph.get_all_connections()

        return sum(
            cost for _, _, cost in connections
        )

    def calculate_cost_reduction(self):

        total_cost = self.calculate_total_network_cost()

        return total_cost - self.mst_cost

    def calculate_savings_percentage(self):

        total_cost = self.calculate_total_network_cost()

        if total_cost == 0:
            return 0

        reduction = self.calculate_cost_reduction()

        return (reduction / total_cost) * 100

    def get_analysis_report(self):

        total_connections = self.graph.get_connection_count()

        mst_connections = len(self.mst_edges)

        return {
            "total_network_cost": self.calculate_total_network_cost(),
            "minimum_network_cost": self.mst_cost,
            "cost_reduction": self.calculate_cost_reduction(),
            "savings_percentage": round(
                self.calculate_savings_percentage(), 2
            ),
            "total_connections": total_connections,
            "mst_connections": mst_connections,
            "unused_connections": (
                total_connections - mst_connections
            )
        }

    def display_report(self):

        report = self.get_analysis_report()

        print("\n========== COST ANALYSIS REPORT ==========")

        for key, value in report.items():
            print(f"{key}: {value}")

        print("==========================================")

        print("[SUCCESS] Cost Analysis completed!")


if __name__ == "__main__":

    print("[INFO] Cost Analysis module loaded successfully!")
