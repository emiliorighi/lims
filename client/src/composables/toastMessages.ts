import { AxiosError } from 'axios'
import { useToast } from 'vuestic-ui/web-components'
import { ErrorResponseData } from '../data/types'

const {init} = useToast()

export function catchError(error: any) {
    const axiosError = error as AxiosError<ErrorResponseData>
    let message
    if (axiosError.response && axiosError.response.status === 401) {
        init({ message: 'Your session has expired. Please login again.', color: 'danger', duration: 3000, closeable:true })
        return //let the interceptor handle it
    }
    if (axiosError.response && axiosError.response.data && axiosError.response.data.message) {
        message = axiosError.response.data.message

    } else {
        message = axiosError.message
    }
    init({ message: message, color: 'danger', duration: 3000, closeable:true })
}

export function success(message:string, duration:number){
    init({message, duration, color:'success'})
}