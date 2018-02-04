<template>
    <section class="chart-container">
        <el-row>
            <el-card class="box_card">
                <div id="faculty_sex" style="width:100%; height:500px;"></div>
            </el-card>
        </el-row>
    </section>
</template>

<script>
    import echarts from 'echarts'
    import { getFacultySex } from '../../api/api';

    export default {
        data() {
            return {
                faculty_sex: null,
                listLoading: true
            }

        },
        methods: {
            drawFacultySex() {
                this.fa_sex = echarts.init(document.getElementById('faculty_sex'));
                //加载数据
                this.listLoading = true;
                getFacultySex().then((res) => {
                    this.listLoading = false;
                    this.fa_sex.setOption(res);
                })
            }
        },
        mounted: function () {
            this.drawFacultySex();
        }
    }
</script>

<style scoped>
    .chart-container {
        margin-top: 20px;
        width: 100%;
        float: left;
    }
</style>