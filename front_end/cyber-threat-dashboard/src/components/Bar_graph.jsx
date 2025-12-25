import {Bar} from 'react-chartjs-2';
import {Chart as Chartjs, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend} from 'chart.js';

Chartjs.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Bar_graph = ({data, chart_label, chart_color}) => {
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
        return {labels: labels, datasets: [{label: chart_label, data: values, borderWidth: 5, backgroundColor: `${chart_color}` , borderColor: `${chart_color}`}]}
    }

    const BarChartData = StandardizeData(data, chart_label, chart_color)
    return (
        <div>
            {<Bar options={{}} data={BarChartData}/>}
        </div>
    )
}

export default Bar_graph