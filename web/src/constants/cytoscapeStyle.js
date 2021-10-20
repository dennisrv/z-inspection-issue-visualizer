const cytoscapeStyle = [
    {
        selector: "node",
        style: {
            "content": "data(label)",
            "height": "50%",
            "width": "130%",
            "text-valign": "center",
            "text-halign": "center",
            "text-wrap": "wrap",
            "text-max-width": "80%",
            "font-size": "11pt",
            "background-color": "#b3b3b3"
        }
    },
    {
        selector: "edge",
        style: {
            "curve-style": "taxi",
            "taxi-direction": "horizontal"
        }
    },
    {
        selector: ".ethical-principle",
        style: {
            "height": "80%",
            "width": "210%",
            // "background-color": "#7C96ED",
            "text-wrap": "wrap",
            "text-max-width": "130%",
            "font-size": "18pt"
        }
    },
    {
        selector: ".key-requirement",
        style: {
            "height": "60%",
            "width": "160%",
            // "background-color": "#7CEDD3",
            "text-wrap": "wrap",
            "text-max-width": "100%",
            "font-size": "14pt"
        }
    },
    {
        selector: ".sub-requirement",
        style: {
            // "background-color": "#96ed7c"
        }
    },
    {
        selector: ".issue",
        style: {
            "shape": "round-rectangle",
            "background-color": "rgba(16,96,5,0.88)"
        }
    },
    {
      selector: ":selected",
      style: {
            "background-blacken": 0.3
      }
    }
]

export const groups = ["technical", "ethical", "medical", "legal", "social"]
const colors = ["#d7191c", "#fdae61", "#ffffbf", "#abdda4", "#2b83ba"]

let group_styles = []
for (let i = 0; i < groups.length; i++) {
    group_styles.push({
        selector: `.${groups[i]}`,
        style: {
            "background-color": colors[i]
        }
    })
}
cytoscapeStyle.push(...group_styles)

export default cytoscapeStyle