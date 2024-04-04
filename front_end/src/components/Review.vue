<script setup lang="ts">
import { GetInfo, PushAudios } from "@/apis/read.js"
import { ref, onMounted, onUnmounted } from 'vue'
import { Mic } from '@element-plus/icons-vue'

let jokes_info = ref()
const recording = ref(false)
const mediaRecorder = ref()
const chunks = ref([])
const audioURL = ref({})
const blob = ref()
const audioText = ref()
const loading = ref(false)
let currentIdx = -1
let stream
const audioSet = new FormData()

onMounted(async () => {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        console.log('授权成功！')
        mediaRecorder.value = new MediaRecorder(stream, { mimeType: 'audio/webm; codecs=opus' })
        mediaRecorder.value.ondataavailable = (e) => {
            chunks.value.push(e.data)
        }

        mediaRecorder.value.onstop = () => {
            blob.value = new Blob(chunks.value, { type: 'audio/webm; codecs=opus' })
            chunks.value = []
            audioURL.value[currentIdx.toString()] = URL.createObjectURL(blob.value)
            audioSet.set(currentIdx.toString(), blob.value, `audio_${currentIdx}.webm`)

        }
    } catch (error) {
        console.error('获取音频输入设备失败：', error)
    }
})

function toggleRecording(idx) {
    if (recording.value) {
        mediaRecorder.value.stop()
        recording.value = false
    } else {
        mediaRecorder.value.start()
        recording.value = true
        currentIdx = idx
    }
}

function closeStream(stream) {
    if (stream) {
        console.log(stream.getTracks())
        stream.getTracks().forEach((track) => track.stop())
    }
}

onUnmounted(() => {
    closeStream(stream)
})

function recite() {
    loading.value = true
    GetInfo({})
        .then((response: any) => {
            loading.value = false
            jokes_info.value = response.data.jokes_info
            console.log("@", jokes_info.value)
        })
        .catch((error: any) => {
            loading.value = false
            console.log("@, error")
        })
}

function submit() {
    loading.value = true
    PushAudios(audioSet)
        .then((response: any) => {
            audioText.value = response.data.audio_text
            loading.value = false
            console.log("@", audioText.value)
        })
        .catch((error: any) => {
            loading.value = false
            console.log("@22, error")
        })
}
</script>

<template>
    <el-button type="primary" @click="recite" v-loading="loading">Recite</el-button>
    <h3 v-if="jokes_info">Today we have {{ jokes_info.length }} Jokes!!</h3>
    <hr />
    <div v-for="(joke, idx) in jokes_info" :key="idx" class="container_cont">
        <div class="each_cont">
            <h4 class="ellipsis">{{ joke }}</h4>
            <el-button type="danger" :icon="Mic" circle @click="toggleRecording(idx)" v-if="!recording" />
            <el-button type="" :icon="Mic" circle @click="toggleRecording(idx)" v-else />
            <audio class="audio-player" controls :src="audioURL[idx.toString()]" preload="auto"></audio>
        </div>
        <div class="each_cont" v-if="audioText && idx in audioText">
            {{ audioText[idx] }}
        </div>
        <hr style="border-top: 1px dashed #000; border-bottom: none;" />
    </div>

    <el-button type="primary" @click="submit" v-loading="loading">Submit</el-button>

</template>

<style>
.ellipsis {
    width: 300px;
    /* 设置一个固定宽度 */
    white-space: nowrap;
    /* 保持文本在同一行 */
    overflow: hidden;
    /* 隐藏溢出部分 */
    text-overflow: ellipsis;
    /* 使用省略号表示溢出部分 */
}
</style>