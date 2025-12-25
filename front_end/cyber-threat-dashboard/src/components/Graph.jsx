import Line_graph from "./Line_graph";
import Bar_graph from "./Bar_graph";
export const Graph = ({data, chart_label, chart_color, chart_type}) => {
    if (chart_type == 'Line')
    {
        return <Line_graph data = {data} chart_label = {chart_label} chart_color = {chart_color}/>
    } else if (chart_type == 'Bar') {
        return(<Bar_graph data = {data} chart_label = {chart_label} chart_color = {chart_color} />)
    } else {
        return(<div></div>)
    }
}
