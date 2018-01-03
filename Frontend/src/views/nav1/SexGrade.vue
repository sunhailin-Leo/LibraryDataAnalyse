<template>
    <section class="chart-container">
        <el-row :gutter="22">
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
                <el-card class="box_card">
                    <div id="sex" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
                <el-card class="box_card">
                    <div id="sex_duplicate" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
        </el-row>
        <el-row>
            <el-col>
                <el-card class="box_card">
                    <div id="grade" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
        </el-row>
    </section>
</template>

<script>
    import echarts from 'echarts'
    import { getSexData, getGradeData, getDuplicateSexData } from '../../api/api';

	export default {
		data() {
			return {
				sex: null,
                sex_dup: null,
                grade: null
			}
		},
		methods: {
			drawSex() {
			    this.sex = echarts.init(document.getElementById('sex'));
			    //加载数据
                this.listLoading = true;
                getSexData().then((res) => {
                    this.listLoading = false;
                    this.sex.setOption(res);
                });
            },
            drawDuplicateSex() {
                this.sex_dup = echarts.init(document.getElementById('sex_duplicate'));
                //加载数据
                this.listLoading = true;
                getDuplicateSexData().then((res) => {
                    this.listLoading = false;
                    this.sex_dup.setOption(res);
                })
            },
            drawGrade() {
                this.grade = echarts.init(document.getElementById('grade'));
                //加载数据
                this.listLoading = true;
                getGradeData().then((res) => {
                    this.listLoading = false;
                    this.grade.setOption(res);
                });
            }
		},
        mounted: function () {
            this.drawSex();
            this.drawDuplicateSex();
            this.drawGrade();
        }
	}

</script>

<style scoped>
    .chart-container {
        margin-top: 20px;
        width: 100%;
        float: left;
    }
    .el-col {
        margin-bottom: 20px;
    }
</style>