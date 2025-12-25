import '../styling/Nav_bar.css'
import { Link } from 'react-router-dom'
const Nav_bar = () => {
  return (
    <div className="navBarContainer">
          <Link to={"/analytics"} className='navigationOptionContainer'>
              <p className="optionText">Insights</p>
          </Link>
         <Link to={"/"} className='navigationOptionContainer'>
              <p className="optionText">Feed</p>
        </Link>
    </div>
  )
}

export default Nav_bar