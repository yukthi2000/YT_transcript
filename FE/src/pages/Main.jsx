import React, { useState } from 'react'
import axios from 'axios'

const Main = () => {
    const [link, setLink] = useState('')
    const [loading , setLoading] = useState(false)
    const[id,setid ]=useState('')

    const handleSubmit = (e) => {
        setLoading(true)
        e.preventDefault()
        axios.post('http://127.0.0.1:5000/link', { link })
        .then((response) => {
            setid(response.data.video_id)
            console.log('====================================');
            console.log(video_id);
            console.log('====================================');
        })
        setLoading(false)
        setLink('')

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
    </div>
  )
}

export default Main
