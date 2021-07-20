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
            "font-size": "11pt"
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
        selector: ".principle",
        style: {
            "height": "80%",
            "width": "210%",
            "background-color": "#7C96ED",
            "text-wrap": "wrap",
            "text-max-width": "130%",
            "font-size": "18pt"
        }
    },
    {
        selector: ".requirement",
        style: {
            "height": "60%",
            "width": "160%",
            "background-color": "#7CEDD3",
            "text-wrap": "wrap",
            "text-max-width": "100%",
            "font-size": "14pt"
        }
    },
    {
        selector: ".sub-requirement",
        style: {
            "background-color": "#96ed7c"
        }
    },
    {
        selector: ".ethical-issue",
        style: {
            "shape": "round-rectangle",
            "background-color": "#ff9980"
        }
    },
    {
        selector: ".flag",
        style: {
            "shape": "round-rectangle",
            "background-color": "#ffea80"
        }
    },
    {
      selector: ":selected",
      style: {
            "background-blacken": 0.3
      }
    }
]

export default cytoscapeStyle