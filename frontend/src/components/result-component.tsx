"use-client"

import { FoodItemVolumeEstimation } from "../models";

const SummaryCard: React.FC<{ summary: string }> = ({ summary }) => (
    <div style={{ border: "1px solid #ccc", padding: "10px", borderRadius: "5px", margin: "10px 0" }}>
      <h2>Summary</h2>
      <p>{summary}</p>
    </div>
  );
  
  const MacrosTable: React.FC<{ foodItems: FoodItemVolumeEstimation[] }> = ({ foodItems }) => (
    <table style={{ borderCollapse: "collapse", width: "100%", margin: "10px 0" }}>
      <thead>
        <tr>
          <th style={{ border: "1px solid #ccc", padding: "8px" }}>Food Item</th>
          <th style={{ border: "1px solid #ccc", padding: "8px" }}>Protein (g)</th>
          <th style={{ border: "1px solid #ccc", padding: "8px" }}>Fat (g)</th>
          <th style={{ border: "1px solid #ccc", padding: "8px" }}>Carbs (g)</th>
          <th style={{ border: "1px solid #ccc", padding: "8px" }}>Fiber (g)</th>
          <th style={{ border: "1px solid #ccc", padding: "8px" }}>Calories</th>
        </tr>
      </thead>
      <tbody>
        {foodItems.map((item, idx) => (
          <tr key={idx}>
            <td style={{ border: "1px solid #ccc", padding: "8px" }}>{item.class_name}</td>
            <td style={{ border: "1px solid #ccc", padding: "8px" }}>{item.macros.protein}</td>
            <td style={{ border: "1px solid #ccc", padding: "8px" }}>{item.macros.fat}</td>
            <td style={{ border: "1px solid #ccc", padding: "8px" }}>{item.macros.carbs}</td>
            <td style={{ border: "1px solid #ccc", padding: "8px" }}>{item.macros.fiber}</td>
            <td style={{ border: "1px solid #ccc", padding: "8px" }}>{item.calories}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
  

export {
    SummaryCard,
    MacrosTable
}