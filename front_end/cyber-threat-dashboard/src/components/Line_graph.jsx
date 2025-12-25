import {Line} from 'react-chartjs-2';
import {Chart as Chartjs, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend} from 'chart.js';

Chartjs.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Line_graph = ({data, chart_label, chart_color}) => {
    const StandardizeData = (data, chart_label, chart_color) => {
        let labels = []
        let values = []
        Object.keys(data).forEach((key => {
            let labelArray = key.split('-')
            if (labelArray.length > 1)
            {
                labels.push(labelArray[1])
            } else{
                labels.push(labelArray[0])
            }
            values.push(data[key])
        }))
        return {labels: labels, datasets: [{label: chart_label, data: values, borderWidth: 5, borderColor: `${chart_color}`}]}
    }

    const lineChartData = StandardizeData(data, chart_label, chart_color)
    return (
        <div>
            {<Line options={{}} data={lineChartData}/>}
        </div>
    )
}

export default Line_graph