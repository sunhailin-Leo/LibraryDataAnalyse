<template>
    <section class="chart-container">
        <el-row>
            <el-col>
                <el-card class="box_card" v-loading="loading">
                    <div id="floor" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
            <el-col>
                <el-card class="box_card" v-loading="loading">
                    <div id="publish" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
            <el-col>
                <el-card class="box_card" v-loading="loading">
                    <div id="author" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
        </el-row>
    </section>
</template>

<script>
	import echarts from 'echarts'
    require('echarts-wordcloud');

	import { getLibDifFloor, getPublishAuthor } from '../../api/api'

	export default {
		data() {
			return {
			    loading: true,
			    lib_floor: null,
                publish: null,
                author: null
			}
		},
		methods: {
		    drawDifFloorInLib() {
                this.lib_floor = echarts.init(document.getElementById('floor'));
                //加载数据
                this.loading = true;
                getLibDifFloor().then((res) => {
                    this.loading = false;
                    this.lib_floor.setOption(res);
                })
            },
            drawPublishAuthorWordCloud() {
                this.publish = echarts.init(document.getElementById('publish'));
                this.author = echarts.init(document.getElementById('author'));

                //加载数据
                this.loading = true;
                getPublishAuthor().then((res) => {
                    this.loading = false;
                    this.publish.setOption(res[0]);
                    this.author.setOption(res[1]);
                    this.author.on('click', function (params) {
                        window.open('https://www.baidu.com/s?wd=' + encodeURIComponent(params.name));
                    });
                    // myChart.on('click', function(params) {
                    //     //alert((params.name));
                    //     window.open('https://www.baidu.com/s?wd=' + encodeURIComponent(params.name));
                    //
                    // });
                })
            }
		},
		mounted() {
		    this.drawDifFloorInLib();
            this.drawPublishAuthorWordCloud();
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