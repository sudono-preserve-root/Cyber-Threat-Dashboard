import {useState, useEffect} from 'react';
import axios from "axios";
import Article_card from '../components/Article_card';
import Overview from '../components/Overview';
import Nav_bar from '../components/Nav_bar';
import '../styling/Feed_page.css';
const feed_page = () => {

  const [articles, set_articles] = useState([]);
  const [offset, update_offset] = useState(0);
  const [level, set_level] = useState('All');
  const [overview_data, update_overview_data] = useState({});

  const FetchArticles = async(limit) => {
    let response = null
    try
    {
        if (level == 'All')
        {
          response = await axios.get(`http://localhost:8000/fetch_articles/${offset}/${limit}`);
        } 
        else 
        {
          response = await axios.get(`http://localhost:8000/fetch_articles/${offset}/${limit}/${level}`)
        }
        console.log(response)
        return response;
    } catch (error)
    {
      console.log(error);
    }
  };

  const FetchAnalyticData = async() => {
    try{
      let response = await axios.get('http://localhost:8000/fetch_analytic_data');
      let data = {
        'total': response.data.total, 
        'critical': response.data.critical, 
        'high': response.data.high, 
        'medium': response.data.medium,
        'low': response.data.low
      }
      update_overview_data(data)
    } catch (error){
      console.log(error)
    }
  }

  const ViewMore = async () => {
    let new_articles = null;
    let article_array = null;
    new_articles = await FetchArticles(30)
    article_array = new_articles.data
    set_articles([...articles, ...article_array])
    update_offset(offset + 30)
  }

  
  useEffect(() => { 
    const InitialFetch = async() => {
    let new_articles = await FetchArticles(30)
    let article_array = new_articles.data
    set_articles([...article_array])
    }
    InitialFetch()
    FetchAnalyticData()
    update_offset(30)
  },[level])

  return (
  <>
  <Nav_bar/>
    {overview_data != null ? 
      <Overview total={overview_data.total} critical={overview_data.critical} high={overview_data.high} medium={overview_data.medium} low={overview_data.low} 
      update_offset={update_offset} set_level={set_level} current_level={level} set_articles={set_articles} ViewMore={ViewMore} articles={articles}/>: <div></div> }
    <div className='feedRow'>
        {articles.length > 0 ? articles.map((article, i) => (
          <div className="feedItem">
            <Article_card 
              date = {article.date}
              description={article.description}
              link = {article.link}
              publisher = {article.publisher}
              severity = {article.severity}
              tags = {article.tags}
              title = {article.title}
              key = {i}
            />
          </div>
        )) : <div></div>}
    </div>
    <div className="addRow">
        <button onClick={ViewMore}>See More Articles</button>
    </div>
  </>
  );
}

export default feed_page