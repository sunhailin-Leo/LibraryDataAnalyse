<template>
    <el-form ref="form" :model="form" label-width="80px">
        <el-row>
            <el-col :span="12">
                <el-form-item label="标题" id="title">
                    <el-input v-model="form.title" placeholder="请输入标题..."></el-input>
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item id="button">
                    <el-button type="primary" @click="submitForm('form')">发布</el-button>
                </el-form-item>
            </el-col>
        </el-row>
        <div id="editor">
            <mavon-editor v-model="form.md_value" style="height: 100%"></mavon-editor>
        </div>
    </el-form>
</template>

<script>
    import { mavonEditor } from 'mavon-editor'

    import 'mavon-editor/dist/css/index.css'
    export default {
        name: 'editor',
        components: {
            mavonEditor
        },
        data() {
            return {
                form: {
                    title: '',
                    md_value: ''
                }
            }
        },
        methods: {
            submitForm: function (formName) {
                let editor_res = this.$refs[formName].model;
                alert(JSON.stringify(editor_res));
            }
            // Balabala function
            // Function--1: Image Uploading (UnComplete)
            // Function--2: Title Save (Complete)
            // Function--3: Body Save (Complete)
            // Function--4: How to upload this Article to MongoDB
            // article_id -> _id; title -> title; md -> content; create_time -> create_time; update_time -> update_time
        }
    }
</script>
<style>
    .el-row {
        margin: auto;
        margin-top: 10px;
    }

    #title {
        margin: auto;
        margin-left: 7%;
        overflow: auto;
        width: 90%;
    }

    #editor {
        margin: auto;
        margin-top: 10px;
        margin-bottom: 20px;
        width: 90%;
        height: 580px;
    }

    #button {
        float: right;
        margin: auto;
        margin-right: 10%;
    }
</style>