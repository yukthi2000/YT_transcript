import React, { useState } from 'react'
import axios from 'axios'

const Main = () => {
    const [link, setLink] = useState('')
    const [loading , setLoading] = useState(false)
    const[id,setid ]=useState('')
    const [error, setError] = useState('')

    const handleSubmit = async(e) => {
        e.preventDefault()

        if(!link)
        {
            setError('Please enter a link')
            return
        }
        setLoading(true)

        setError('')
        try{

      const response = await axios.post('http://127.0.0.1:5000/link', { link })
      setid(response.data.video_id)
      console.log(response.data.video_id)
        }catch (error) {
            setError(error.response?.data?.error||'Error fetching data') 
            console.log('====================================');
            console.log(error);
            console.log('====================================');
        }
        finally {
            setLoading(false)
        }
        // setLoading(false)
 

    }

    const handleChange = (e) => {
        setLink(e.target.value)
    }


  return (
    <div>
        <span>Enter the yt link</span>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Enter the yt link" onChange={handleChange}/>
        <button type="submit" >Submit</button>

      </form>

      {error && (
        <div className="error">{error}</div>
      )}

      {id && (
        <div className="success">Your link is: {id}
        <iframe width="560" height="315" src={`https://www.youtube.com/embed/${id}`} title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
        </div>   
    )}
    </div>
  )
}

export default Main
