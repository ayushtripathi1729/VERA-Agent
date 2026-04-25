from datetime import datetime
from typing import List, Any


class NeuralReporter:
    """
    Synthesis & Formatting Engine for V.E.R.A.
    Produces clean, structured, and demo-friendly execution reports.
    """

    def __init__(self):
        self.node_id = "JKIAPT_PRAYAGRAJ_NODE_01"

    def generate_executive_summary(
        self,
        instruction: str,
        output: str,
        steps: List[Any] = None
    ) -> str:
        """
        Generates a structured execution report.
        """

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = []

        # 🔷 HEADER
        report.append("🧠 V.E.R.A EXECUTION REPORT")
        report.append(f"⏱ Timestamp: {timestamp}")
        report.append(f"🖥 Node: {self.node_id}")
        report.append(f"👤 Operator: Ayush Tripathi")
        report.append("-" * 50)

        # 🎯 GOAL
        report.append("🎯 OBJECTIVE:")
        report.append(f"{instruction}")
        report.append("-" * 50)

        # ⚙️ STEPS
        if steps:
            report.append("⚙️ EXECUTION TRACE:")

            for i, step_data in enumerate(steps):
                try:
                    # step_data is (description, result)
                    description, result = step_data

                    # Trim long outputs
                    result_str = str(result)
                    if len(result_str) > 150:
                        result_str = result_str[:150] + "..."

                    report.append(f"\nStep {i+1}:")
                    report.append(f"→ Task: {description}")
                    report.append(f"→ Result: {result_str}")

                except Exception:
                    report.append(f"\nStep {i+1}: [UNREADABLE STEP DATA]")

            report.append("-" * 50)

        # ✅ FINAL OUTPUT
        report.append("✅ FINAL OUTPUT:")
        report.append(output)

        report.append("-" * 50)
        report.append("🔚 END OF REPORT")

        return "\n".join(report)

    def format_error(self, error_msg: str) -> str:
        """
        Standardized error format.
        """

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (
            "🚨 V.E.R.A SYSTEM ERROR\n"
            f"⏱ Timestamp: {timestamp}\n"
            f"🖥 Node: {self.node_id}\n"
            f"❌ Error: {error_msg}\n"
        )


# Singleton instance
vera_reporter = NeuralReporter()
