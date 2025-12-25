import '../styling/Article_card.css'
import Tag_card from './Tag_card'
import Severity_tag from './Severity_tag'

const Article_card = ({date, description, link, publisher, severity, tags, title, id}) => {
  return (
    <a href={link} target='_blank'>
        <div className="card">
            <div className="title">
                {title}
            </div>
            <div className="upperRow">
                <div className="publisher">{publisher}</div>
                <div className="date">{date}</div>
            </div>
            <div className="severity"><Severity_tag level = {severity} key = {id}/></div>
            <div className="tagRow">
              {tags.map((tag_name, i) => (
                <div className="tag"><Tag_card name = {tag_name} key = {i}/></div>
              ))}
            </div>
            <div className="description">{description}</div>
        </div>
    </a>
  )
}

export default Article_card