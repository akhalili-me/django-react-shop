import React,{useEffect} from 'react'
import { Alert } from 'react-bootstrap'
import { useSelector,useDispatch } from 'react-redux'
import { hideAlarm } from '../../features/alert/alarmSlice'

const Alarm = () => {
  const { message, type, show } = useSelector((state) => state.alarm);
  const dispatch = useDispatch()

  useEffect(() => {
    if (show) {
      setTimeout(() => dispatch(hideAlarm()),3000)
    }
  }, [show,dispatch])
  
  return (
    <>    
      { show &&  
        <Alert variant={type} className='global_alarm' >
          {message}
        </Alert>
      }
    </>
  )
}

export default Alarm