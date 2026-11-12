import sys
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk
import networkx as nx

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Project root configuration
PROJECT_ROOT = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.network_manager import NetworkManager
from core.prims import PrimsAlgorithm
from analysis.cost_analysis import CostAnalysis


# THEME CONFIGURATION
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NetOptimaApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("NetOptima | Network Optimization System")
        self.geometry("1400x850")
        self.minsize(1100, 700)

        self.C = {
            "bg": "#0B1220",
            "sidebar": "#101B2D",
            "card": "#16243A",
            "card2": "#1C2D46",
            "blue": "#3B82F6",
            "green": "#22C55E",
            "text": "#F1F5F9",
            "muted": "#94A3B8",
            "border": "#263850",
            "yellow": "#FBBF24",
            "grey": "#64748B",
            "red": "#F87171"
        }

        self.configure(fg_color=self.C["bg"])

        self.data_file = PROJECT_ROOT / "data" / "network.json"

        self.manager = NetworkManager()

        self.load_or_create_demo_network()

        self.setup_ui()
        self.show_dashboard()

    # LOAD NETWORK
    def load_or_create_demo_network(self):

        if self.data_file.exists():

            try:
                self.manager.load_network(str(self.data_file))

                if self.manager.graph.get_location_count() > 0:
                    return

            except (ValueError, KeyError, TypeError, OSError) as error:
                print("[WARNING] Saved network could not be loaded:", error)

        self.create_demo_network()

    # DEMO NETWORK
    def create_demo_network(self):

        self.manager = NetworkManager()

        self.manager.add_connection(
            "Hospital", "University", 20000
        )

        self.manager.add_connection(
            "Hospital", "School", 15000
        )

        self.manager.add_connection(
            "University", "Data Center", 25000
        )

        self.manager.add_connection(
            "School", "Data Center", 10000
        )

        print("[SUCCESS] Demo network created!")

    # MAIN UI
    def setup_ui(self):

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0,
            fg_color=self.C["sidebar"]
        )

        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="NETOPTIMA",
            font=("Arial", 25, "bold"),
            text_color=self.C["blue"]
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            self.sidebar,
            text="Network Optimization",
            font=("Arial", 11),
            text_color=self.C["muted"]
        ).pack(pady=(0, 35))

        self.add_nav_button("Dashboard", self.show_dashboard)
        self.add_nav_button("Network Management", self.show_network)
        self.add_nav_button("Optimization", self.show_optimization)
        self.add_nav_button("Cost Analysis", self.show_cost_analysis)

        spacer = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        spacer.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self.sidebar,
            text="Prim's MST Engine",
            text_color=self.C["muted"],
            font=("Arial", 11)
        ).pack(pady=20)

        # MAIN CONTENT
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=self.C["bg"],
            corner_radius=0
        )

        self.main_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=20,
            pady=20
        )

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        self.page_heading = ctk.CTkLabel(
            self.header,
            text="Dashboard",
            font=("Arial", 27, "bold"),
            text_color=self.C["text"]
        )
        self.page_heading.pack(side="left")

        self.content_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    # NAVIGATION BUTTON
    def add_nav_button(self, title, command):

        button = ctk.CTkButton(
            self.sidebar,
            text=title,
            command=command,
            height=45,
            corner_radius=9,
            fg_color="transparent",
            hover_color=self.C["card2"],
            text_color=self.C["text"],
            anchor="w",
            font=("Arial", 14)
        )

        button.pack(fill="x", padx=15, pady=5)

    # CLEAR PAGE
    def clear_content(self):

        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # PAGE TITLE
    def page_title(self, title):

        self.page_heading.configure(text=title)
        self.clear_content()

    # MST HELPER
    def get_mst(self):

        graph = self.manager.graph

        if graph.get_location_count() == 0:
            raise ValueError("No network locations available.")

        start = next(iter(graph.adjacency_list))

        algorithm = PrimsAlgorithm(graph)

        return algorithm.find_mst(start)

    # KPI CARD
    def create_metric_card(self, parent, title, value, column):

        card = ctk.CTkFrame(
            parent,
            fg_color=self.C["card"],
            corner_radius=13
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color=self.C["muted"],
            font=("Arial", 12)
        ).pack(pady=(17, 7))

        ctk.CTkLabel(
            card,
            text=str(value),
            text_color=self.C["text"],
            font=("Arial", 23, "bold")
        ).pack(pady=(0, 17))

        return card

    # DASHBOARD
    def show_dashboard(self):

        self.page_title("Dashboard")

        graph = self.manager.graph

        locations = graph.get_location_count()
        connections = graph.get_connection_count()

        try:
            mst_edges, mst_cost = self.get_mst()
            mst_count = len(mst_edges)

        except ValueError:
            mst_edges = []
            mst_cost = 0
            mst_count = 0

        total_cost = sum(
            cost for _, _, cost in graph.get_all_connections()
        )

        metrics_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        metrics_frame.pack(fill="x", pady=5)

        for column in range(4):
            metrics_frame.grid_columnconfigure(column, weight=1)

        self.create_metric_card(
            metrics_frame, "Locations", locations, 0
        )

        self.create_metric_card(
            metrics_frame, "Connections", connections, 1
        )

        self.create_metric_card(
            metrics_frame, "MST Connections", mst_count, 2
        )

        self.create_metric_card(
            metrics_frame,
            "Minimum Cost",
            f"Rs. {mst_cost:,.0f}",
            3
        )

        # GRAPH SECTION
        graph_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.C["card"],
            corner_radius=15
        )

        graph_card.pack(fill="both", expand=True, pady=15)

        ctk.CTkLabel(
            graph_card,
            text="Network Infrastructure Visualization",
            font=("Arial", 19, "bold"),
            text_color=self.C["text"]
        ).pack(pady=15)

        figure = Figure(figsize=(9, 4.5), dpi=100)
        ax = figure.add_subplot(111)

        figure.patch.set_facecolor(self.C["card"])
        ax.set_facecolor(self.C["card"])

        G = nx.Graph()

        for location in graph.adjacency_list:
            G.add_node(location)

        for source, destination, cost in graph.get_all_connections():
            G.add_edge(source, destination, weight=cost)

        if G.number_of_nodes() > 0:

            pos = nx.spring_layout(G, seed=42)

            nx.draw_networkx_nodes(
                G, pos, ax=ax,
                node_color="#3B82F6",
                node_size=2200
            )

            nx.draw_networkx_labels(
                G, pos, ax=ax,
                font_color="white",
                font_size=9
            )

            mst_set = {
                frozenset((u, v))
                for u, v, _ in mst_edges
            }

            for source, destination, data in G.edges(data=True):

                is_mst = frozenset((source, destination)) in mst_set

                nx.draw_networkx_edges(
                    G, pos,
                    edgelist=[(source, destination)],
                    ax=ax,
                    edge_color="#22C55E" if is_mst else "#64748B",
                    width=3 if is_mst else 1.5,
                    style="solid" if is_mst else "dashed"
                )

            edge_labels = nx.get_edge_attributes(G, "weight")
            edge_labels = {
    (source, destination): f"Rs. {cost:,.0f}"
    for source, destination, cost
    in self.manager.graph.get_all_connections()
}

            # nx.draw_networkx_edge_labels(
            #     G, pos,
            #     edge_labels=edge_labels,
            #     ax=ax,
            #     font_color="white",
            #     font_size=8
            # )
            nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=9,
    font_color="#FFFFFF",
    font_weight="bold",
    rotate=False,
    bbox=dict(
        facecolor="#172B45",
        edgecolor="#64748B",
        alpha=0.95,
        pad=3
    ),
    ax=ax
)

        ax.axis("off")
        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=graph_card
        )

        canvas.draw()
        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # COST SUMMARY
        summary = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.C["card"],
            corner_radius=12
        )
        summary.pack(fill="x", pady=10)

        reduction = total_cost - mst_cost

        percentage = (
            reduction / total_cost * 100
            if total_cost > 0 else 0
        )

        ctk.CTkLabel(
            summary,
            text=(
                f"Total Available Cost: Rs. {total_cost:,.2f}    |    "
                f"Minimum Cost: Rs. {mst_cost:,.2f}    |    "
                f"Cost Reduction: Rs. {reduction:,.2f}    |    "
                f"Savings: {percentage:.2f}%"
            ),
            text_color=self.C["green"],
            font=("Arial", 14, "bold")
        ).pack(pady=18)

    # NETWORK MANAGEMENT PAGE
    def show_network(self):

        self.page_title("Network Management")

        # ADD LOCATION
        location_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.C["card"],
            corner_radius=12
        )
        location_card.pack(fill="x", pady=10)

        ctk.CTkLabel(
            location_card,
            text="Add New Location",
            font=("Arial", 18, "bold")
        ).pack(pady=12)

        self.location_entry = ctk.CTkEntry(
            location_card,
            placeholder_text="Enter location name",
            width=300
        )
        self.location_entry.pack(pady=5)

        ctk.CTkButton(
            location_card,
            text="Add Location",
            command=self.add_location_ui
        ).pack(pady=12)

        # ADD CONNECTION
        connection_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.C["card"],
            corner_radius=12
        )
        connection_card.pack(fill="x", pady=10)

        ctk.CTkLabel(
            connection_card,
            text="Add Network Connection",
            font=("Arial", 18, "bold")
        ).pack(pady=12)

        self.source_entry = ctk.CTkEntry(
            connection_card,
            placeholder_text="Source location",
            width=300
        )
        self.source_entry.pack(pady=5)

        self.destination_entry = ctk.CTkEntry(
            connection_card,
            placeholder_text="Destination location",
            width=300
        )
        self.destination_entry.pack(pady=5)

        self.cost_entry = ctk.CTkEntry(
            connection_card,
            placeholder_text="Installation cost",
            width=300
        )
        self.cost_entry.pack(pady=5)

        ctk.CTkButton(
            connection_card,
            text="Add Connection",
            command=self.add_connection_ui
        ).pack(pady=12)

        # CURRENT NETWORK
        network_card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.C["card"],
            corner_radius=12
        )
        network_card.pack(fill="x", pady=10)

        ctk.CTkLabel(
            network_card,
            text="Current Network",
            font=("Arial", 18, "bold")
        ).pack(pady=12)

        self.network_list = ctk.CTkFrame(
            network_card,
            fg_color="transparent"
        )
        self.network_list.pack(fill="x", padx=15, pady=10)

        # SAVE AND LOAD
        controls = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        controls.pack(fill="x", pady=15)

        ctk.CTkButton(
            controls,
            text="Save Network",
            command=self.save_network_ui
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            controls,
            text="Load Network",
            command=self.load_network_ui
        ).pack(side="left", padx=10)

        self.refresh_network_lists()

    # REFRESH NETWORK
    def refresh_network_lists(self):

        if not hasattr(self, "network_list"):
            return

        for widget in self.network_list.winfo_children():
            widget.destroy()

        graph = self.manager.graph

        for location in graph.adjacency_list:

            row = ctk.CTkFrame(
                self.network_list,
                fg_color=self.C["card2"],
                corner_radius=8
            )
            row.pack(fill="x", pady=4)

            ctk.CTkLabel(
                row,
                text=location,
                text_color=self.C["text"]
            ).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(
                row,
                text="Delete",
                width=80,
                fg_color=self.C["red"],
                hover_color="#DC2626",
                command=lambda name=location:
                    self.delete_location_ui(name)
            ).pack(side="right", padx=10, pady=5)

        for source, destination, cost in graph.get_all_connections():

            row = ctk.CTkFrame(
                self.network_list,
                fg_color=self.C["card2"],
                corner_radius=8
            )
            row.pack(fill="x", pady=4)

            ctk.CTkLabel(
                row,
                text=f"{source} <-> {destination} | Rs. {cost:,.2f}",
                text_color=self.C["text"]
            ).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(
                row,
                text="Remove Link",
                width=100,
                command=lambda a=source, b=destination:
                    self.delete_connection_ui(a, b)
            ).pack(side="right", padx=10, pady=5)

    # ADD LOCATION UI
    def add_location_ui(self):

        location = self.location_entry.get().strip()

        try:
            self.manager.add_location(location)

            messagebox.showinfo(
                "Success",
                f"Location added: {location}"
            )

            self.location_entry.delete(0, "end")
            self.refresh_network_lists()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    # ADD CONNECTION UI
    def add_connection_ui(self):

        source = self.source_entry.get().strip()
        destination = self.destination_entry.get().strip()
        cost_text = self.cost_entry.get().strip()

        try:
            cost = float(cost_text)

            if cost.is_integer():
                cost = int(cost)

            self.manager.add_connection(
                source,
                destination,
                cost
            )

            messagebox.showinfo(
                "Success",
                "Network connection added successfully!"
            )

            self.source_entry.delete(0, "end")
            self.destination_entry.delete(0, "end")
            self.cost_entry.delete(0, "end")

            self.refresh_network_lists()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    # DELETE LOCATION
    def delete_location_ui(self, location):

        confirm = messagebox.askyesno(
            "Confirm",
            f"Delete location {location}?"
        )

        if not confirm:
            return

        try:
            self.manager.remove_location(location)

            self.refresh_network_lists()

            messagebox.showinfo(
                "Success",
                "Location deleted successfully!"
            )

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    # DELETE CONNECTION
    def delete_connection_ui(self, source, destination):

        confirm = messagebox.askyesno(
            "Confirm",
            f"Remove connection {source} <-> {destination}?"
        )

        if not confirm:
            return

        try:
            self.manager.remove_connection(source, destination)

            self.refresh_network_lists()

            messagebox.showinfo(
                "Success",
                "Connection removed successfully!"
            )

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    # SAVE NETWORK
    def save_network_ui(self):

        try:
            self.manager.save_network(str(self.data_file))

            messagebox.showinfo(
                "Success",
                "Network saved successfully!"
            )

        except (OSError, ValueError, TypeError) as error:
            messagebox.showerror("Save Error", str(error))

    # LOAD NETWORK
    def load_network_ui(self):

        try:
            if not self.data_file.exists():
                messagebox.showwarning(
                    "Warning",
                    "No saved network file found."
                )
                return

            self.manager.load_network(str(self.data_file))

            self.refresh_network_lists()

            messagebox.showinfo(
                "Success",
                "Network loaded successfully!"
            )

        except (OSError, ValueError, KeyError, TypeError) as error:
            messagebox.showerror("Load Error", str(error))

    # OPTIMIZATION PAGE
    def show_optimization(self):

        self.page_title("Network Optimization")

        try:
            mst_edges, mst_cost = self.get_mst()

        except ValueError as error:

            ctk.CTkLabel(
                self.content_frame,
                text=str(error),
                text_color=self.C["red"]
            ).pack(pady=30)

            return

        card = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.C["card"],
            corner_radius=15
        )
        card.pack(fill="x", pady=15)

        ctk.CTkLabel(
            card,
            text="Prim's Minimum Spanning Tree",
            font=("Arial", 21, "bold")
        ).pack(pady=20)

        for source, destination, cost in mst_edges:

            ctk.CTkLabel(
                card,
                text=f"{source}  ->  {destination}     Rs. {cost:,.2f}",
                font=("Arial", 15),
                text_color=self.C["green"]
            ).pack(pady=8)

        ctk.CTkLabel(
            card,
            text=f"Minimum Network Cost: Rs. {mst_cost:,.2f}",
            font=("Arial", 20, "bold"),
            text_color=self.C["green"]
        ).pack(pady=20)

        ctk.CTkLabel(
            self.content_frame,
            text="The MST connects all locations using the minimum total edge cost.",
            font=("Arial", 13),
            text_color=self.C["muted"]
        ).pack(pady=10)

    # COST ANALYSIS PAGE
    def show_cost_analysis(self):

        self.page_title("Cost Analysis")

        try:
            mst_edges, mst_cost = self.get_mst()

            analysis = CostAnalysis(
                self.manager.graph,
                mst_edges,
                mst_cost
            )

            report = analysis.get_analysis_report()

        except ValueError as error:

            ctk.CTkLabel(
                self.content_frame,
                text=f"Unable to generate report: {error}",
                text_color=self.C["red"]
            ).pack(pady=30)

            return

        ctk.CTkLabel(
            self.content_frame,
            text="Network Cost Analysis Report",
            font=("Arial", 22, "bold"),
            text_color=self.C["text"]
        ).pack(pady=20)

        metrics = [
            ("Total Network Cost",
             f"Rs. {report['total_network_cost']:,.2f}"),

            ("Minimum Network Cost",
             f"Rs. {report['minimum_network_cost']:,.2f}"),

            ("Cost Reduction",
             f"Rs. {report['cost_reduction']:,.2f}"),

            ("Savings Percentage",
             f"{report['savings_percentage']}%"),

            ("Total Connections",
             str(report["total_connections"])),

            ("MST Connections",
             str(report["mst_connections"])),

            ("Unused Alternative Connections",
             str(report["unused_connections"]))
        ]

        cards_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        cards_frame.pack(fill="x", padx=10, pady=10)

        for column in range(2):
            cards_frame.grid_columnconfigure(column, weight=1)

        for index, (label, value) in enumerate(metrics):

            card = ctk.CTkFrame(
                cards_frame,
                fg_color=self.C["card"],
                corner_radius=12
            )

            card.grid(
                row=index // 2,
                column=index % 2,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            ctk.CTkLabel(
                card,
                text=label,
                text_color=self.C["muted"],
                font=("Arial", 13)
            ).pack(pady=(15, 5))

            ctk.CTkLabel(
                card,
                text=value,
                text_color=self.C["green"],
                font=("Arial", 21, "bold")
            ).pack(pady=(5, 15))

        details = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.C["card"],
            corner_radius=12
        )
        details.pack(fill="x", padx=10, pady=15)

        ctk.CTkLabel(
            details,
            text="Minimum Spanning Tree Connections",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        for source, destination, cost in mst_edges:

            ctk.CTkLabel(
                details,
                text=f"{source} -> {destination} | Rs. {cost:,.2f}",
                text_color=self.C["green"],
                font=("Arial", 14)
            ).pack(pady=5)

        print("[SUCCESS] Cost Analysis Dashboard loaded!")


# APPLICATION ENTRY POINT
if __name__ == "__main__":

    print("\n========== NETOPTIMA APPLICATION ==========")

    app = NetOptimaApp()

    print("[SUCCESS] NetOptima dashboard initialized!")

    app.mainloop()
