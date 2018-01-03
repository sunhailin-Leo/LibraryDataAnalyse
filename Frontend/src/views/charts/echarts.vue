<template>
    <section class="chart-container">
        <section class="content">
            <el-card class="box_card">
                <div class="col-md-3 col-sm-6 col-xs-12">
                    <div class="info-box">
                        <span class="info-box-icon bg-aqua"><i class="fa fa-book"></i></span>
                        <div class="info-box-content">
                            <p></p>
                            <span class="info-box-text">总借阅记录数</span>
                            <span class="info-box-number">{{ borrowTotal }}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6 col-xs-12">
                    <div class="info-box">
                        <span class="info-box-icon bg-red"><i class="fa fa-users"></i></span>

                        <div class="info-box-content">
                            <p></p>
                            <span class="info-box-text">教职工借书人数</span>
                            <span class="info-box-number">{{ TeacherCount }}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6 col-xs-12">
                    <div class="info-box">
                        <span class="info-box-icon bg-green"><i class="fa fa-users"></i></span>

                        <div class="info-box-content">
                            <p></p>
                            <span class="info-box-text">广商学生借书人数</span>
                            <span class="info-box-number">{{ GzccStuCount }}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 col-sm-6 col-xs-12">
                    <div class="info-box">
                        <span class="info-box-icon bg-yellow"><i class="fa fa-users"></i></span>

                        <div class="info-box-content">
                            <p></p>
                            <span class="info-box-text">职院学生借书人数</span>
                            <span class="info-box-number">{{ KdStuCount}}</span>
                        </div>
                    </div>
                </div>
            </el-card>
        </section>
        <el-row :gutter="22">
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
                <el-card class="box_card">
                    <div id="gzccTop15" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
                <el-card class="box_card">
                    <div id="kdTop15" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
        </el-row>
        <el-row :gutter="22">
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
                <el-card class="box_card">
                    <div id="difFacultyGzcc" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
            <el-col :xs="24" :sm="24" :md="12" :lg="12">
                <el-card class="box_card">
                    <div id="difFacultyKd" style="width:100%; height:400px;"></div>
                </el-card>
            </el-col>
        </el-row>
    </section>
</template>

<script>
    import echarts from 'echarts'
    import { getLibraryBorrowPeopleType, getGzccTop15, getKdTop15, getGzccDifFaculty, getKdDifFaculty } from '../../api/api';

    export default {
        data() {
            return {
                gzccTop15: null,
                kdTop15: null,
                gzccdifFaculty: null,
                kddifFaculty: null,

                total: {
                    borrowTotal: 0,
                    TeacherCount: 0,
                    GzccStuCount: 0,
                    KdStuCount: 0
                },
            }
        },
        computed: {
            borrowTotal() {
                // 借阅总数
                return this.total.borrowTotal;
            },
            /**
             * @return {number}
             */
            TeacherCount() {
                // 计算属性: 昨天的用户总数
                return this.total.TeacherCount;
            },
            /**
             * @return {number}
             */
            GzccStuCount() {
                // 计算属性: 7天内的用户总数
                return this.total.GzccStuCount;
            },
            /**
             * @return {number}
             */
            KdStuCount() {
                // 计算属性: 30天内的用户总数
                return this.total.KdStuCount;
            },
        },
        methods: {
            getPeopleCount() {
                // 加载数据
                this.listLoading = true;
                getLibraryBorrowPeopleType().then((res) => {
                    this.listLoading = false;
                    this.total.borrowTotal = eval(res.join("+"));
                    this.total.GzccStuCount = res[0];
                    this.total.KdStuCount = res[1];
                    this.total.TeacherCount = res[2];
                });
            },
            drawGzccTop15() {
                this.gzccTop15 = echarts.init(document.getElementById('gzccTop15'));
                //加载数据
                this.listLoading = true;
                getGzccTop15().then((res) => {
                   this.listLoading = false;
                   this.gzccTop15.setOption(res);
                });
            },
            drawKdTop15() {
                this.kdTop15 = echarts.init(document.getElementById('kdTop15'));
                //加载数据
                this.listLoading = true;
                getKdTop15().then((res) => {
                    this.listLoading = false;
                    this.kdTop15.setOption(res);
                });
            },
            drawGzccDifFaculty() {
                this.gzccdifFaculty = echarts.init(document.getElementById('difFacultyGzcc'));
                this.listLoading = true;
                getGzccDifFaculty().then((res) => {
                    this.listLoading = false;
                    this.gzccdifFaculty.setOption(res);
                });
            },
            drawKdDifFaculty(){
                this.kddifFaculty = echarts.init(document.getElementById('difFacultyKd'));
                this.listLoading = true;
                getKdDifFaculty().then((res) => {
                    this.listLoading = false;
                    this.kddifFaculty.setOption(res);
                })
            },

            // 根方法
            drawCharts() {
                this.getPeopleCount();
                this.drawGzccTop15();
                this.drawKdTop15();
                this.drawGzccDifFaculty();
                this.drawKdDifFaculty();
            },
        },
        mounted: function () {
            this.drawCharts()
        },
        // updated: function () {
        //     this.drawCharts()
        // }
    }
</script>

<style scoped>
    .chart-container {
        width: 100%;
        float: left;
    }
    .info-box {
        cursor: pointer;
    }
    .el-col {
        margin-bottom: 20px;
    }
    .info-box-content {
        text-align: center;
        vertical-align: middle;
        display: inherit;
    }
    .info-box {
        cursor: pointer;
    }

    .content {
        min-height: 100px;
    }
</style>
