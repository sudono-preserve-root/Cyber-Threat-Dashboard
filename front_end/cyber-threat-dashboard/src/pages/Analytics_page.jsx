import { useEffect, useState } from "react";
import axios from 'axios';
import { Graph } from "../components/Graph";
import '../styling/Analytics_page.css';
import Nav_bar from "../components/Nav_bar";
const Analytics_page = () => {
    const [yearlyData, setYearlyData] = useState({})
    const [yearlyDataChartGraph, setYearlyDataChartGraph] = useState('Line')
    const [yearlyTagOverviewGraph, setYearlyTagOverviewGraph] = useState('Line')
    const [yearlyDataChartGraphColor, setYearlyDataChartGraphColor] = useState('#E6E6FA')
    const [yearlyTagOverviewGraphColor, setYearlyTagOverviewGraphColor] = useState('#E6E6FA')
    const [yearlyTagData, setYearlyTagData] = useState({})
    
   const FetchYearlyData = async() => {
        let response = await axios.get('http://localhost:8000/fetch_monthly_analytics');
        return response
   }

   const FetchYearlyTagData = async() => {
        let response = await axios.get('http://localhost:8000/fetch_tag_analytics')
        return response
   }

   const ModifyYearlyDataGraph = () => {
        setYearlyDataChartGraph(document.getElementById('chartThreatOverview').value)
   }

   const ModifyYearlyDataGraphColor = () => {
        setYearlyDataChartGraphColor(document.getElementById('colorThreatOverview').value)
   }
   
   const ModifyYearlyTagDataGraph = () => {
        setYearlyTagOverviewGraph(document.getElementById('chartTagOverview').value)
   }

   const ModifyYearlyTagDataGraphColor = () => {
        setYearlyTagOverviewGraphColor(document.getElementById('colorTagOverview').value)
   }

   useEffect(() => {
    const InitialFetch = async() => {
        let yearlyDataResponse = await FetchYearlyData()
        let yearlyTagDataResponse = await FetchYearlyTagData()
        let yearlyObject = {}
        let tagObject = {}

        Object.keys(yearlyDataResponse.data).forEach((key) => {
            let keyArray = key.split('-')
            let newKey = `${keyArray[0]}-${keyArray[1]}`
            yearlyObject[newKey] = yearlyDataResponse.data[key]
        })

        Object.keys(yearlyTagDataResponse.data).forEach((key) => {
            if (yearlyTagDataResponse.data[key] > 0)
            {
                let newKey = ''
                let keyArray = key.split('-')
                if (keyArray[1] == "CVE")
                {
                    newKey = `${keyArray[1]} ${keyArray[2]} ${keyArray[3]}`
                }
                else if (keyArray.length == 3){
                    newKey = `${keyArray[1]}`
                }
                else{
                    newKey = `${keyArray[1]} ${keyArray[2]}`
                }
                tagObject[newKey] = yearlyTagDataResponse.data[key]
            }
        })
        setYearlyData(yearlyObject)
        setYearlyTagData(tagObject)
    }

    InitialFetch()
   }, [])

  return (
    <>
    <Nav_bar />
    <div className="analyticsMasterContainer">
        <div className="titleContainer">
            <p className="Title">Threats Scanned Overview For {new Date().getFullYear()}</p>
            <select name="charts" id="chartThreatOverview" onChange={ModifyYearlyDataGraph}>
                <option value="Line">Line</option>
                <option value="Bar">Bar</option>
            </select>
            <input type="color" id="colorThreatOverview" value={yearlyDataChartGraphColor} onChange={ModifyYearlyDataGraphColor}/>
        </div>
        {Object.keys(yearlyData).length > 0 ? <Graph data={yearlyData} chart_label={"Months"} chart_color={yearlyDataChartGraphColor} chart_type={yearlyDataChartGraph}/>: <div></div>}
        <div className="titleContainer">
            <p className="Title">Tag Distribution Overview {new Date().getFullYear()}</p>
            <select name="charts" id="chartTagOverview" onChange={ModifyYearlyTagDataGraph}>
                <option value="Line">Line</option>
                <option value="Bar">Bar</option>
            </select>
            <input type="color" id="colorTagOverview" value={yearlyTagOverviewGraphColor} onChange={ModifyYearlyTagDataGraphColor}/>
        </div>
        {Object.keys(yearlyTagData).length > 0 ? <Graph data={yearlyTagData} chart_label={"Tag"} chart_color={yearlyTagOverviewGraphColor} chart_type={yearlyTagOverviewGraph}/> : <div></div>}
    </div>
    </>
  )
}

export default Analytics_page