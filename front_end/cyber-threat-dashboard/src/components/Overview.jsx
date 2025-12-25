import '../styling/Overview.css'
const Overview = ({total, critical, high, medium, low, update_offset, current_level, set_level, set_articles}) => {
  const determine_query_level = (level) => {
    if (current_level != level)
    {
        update_offset(0)
        set_level(level)
        set_articles([])
    }
  }
  return (
    <div className="overViewContainer">
        <div className="statContainer" onClick={() => {determine_query_level('All')}} >
            <p>{total}</p>
            <p>Total Threats</p>
        </div>
        <div className="statContainer" onClick={() => {determine_query_level('Critical')}}>
            <p>{critical}</p>
            <p>Critical Threats</p>
        </div>
        <div className="statContainer" onClick={() => {determine_query_level('High')}}>
            <p>{high}</p>
            <p>High Threats</p>
        </div>
        <div className="statContainer" onClick={() => {determine_query_level('Medium')}}>
            <p>{medium}</p>
            <p>Medium Threats</p>
        </div>
        <div className="statContainer" onClick={() => {determine_query_level('Low')}}>
            <p>{low}</p>
            <p>Low Threats</p>
        </div>
    </div>
  )
}

export default Overview