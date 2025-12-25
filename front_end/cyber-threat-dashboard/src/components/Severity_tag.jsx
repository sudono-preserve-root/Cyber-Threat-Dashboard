const Severity_tag = ({level}) => {
    if(level === "Low")
    {
        return(<div style={{color: 'green', padding: '.25vw', border: '.1vw solid rgb(0, 0, 0)', borderRadius: '15%'}}>{level}</div>);
    } else if (level == 'Medium')
    {
        return(<div style={{color: 'orange', padding: '.25vw', border: '.1vw solid rgb(0, 0, 0)', borderRadius: '15%'}}>{level}</div>);
    } else if (level == 'High')
    {
        return(<div style={{color: 'red', padding: '.25vw', border: '.1vw solid rgb(0, 0, 0)', borderRadius: '15%'}}>{level}</div>);
    } else 
    {
        return(<div style={{color: 'purple', padding: '.25vw', border: '.1vw solid rgb(0, 0, 0)', borderRadius: '15%'}}>{level}</div>);
    }
}

export default Severity_tag