import service from "@/utils/request.js"

export function PushJoke(updateData){
    return service.request({
        method: "post",
        url: "/push_joke",
        data: updateData
    })
}

export function PushAudios(postData){
    return service.request({
        method: "post",
        url: "/post_audios",
        data: postData,
    })
}

export function GetInfo(getParams){
    return service.request({
        method: "get",
        url: "/get_today_info",
        params: getParams
    })
}