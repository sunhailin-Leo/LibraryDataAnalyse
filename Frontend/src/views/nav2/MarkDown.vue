<template>
    <div id="editor">
        <mavon-editor style="height: 100%"></mavon-editor>
    </div>
</template>

<script>
    import { mavonEditor } from 'mavon-editor'

    import 'mavon-editor/dist/css/index.css'
    export default {
        name: 'editor',
        components: {
            mavonEditor
            // or 'mavon-editor': mavonEditor
        }
    }
</script>
<style>
    #editor {
        margin: auto;
        width: 80%;
        height: 580px;
    }
</style>