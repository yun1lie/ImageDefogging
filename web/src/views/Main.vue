<template>
  <el-main>
    <div class="main-container">
      <Upload />
      <Preview />
      <Parameters />
    </div>
  </el-main>
</template>

<script>
import Upload from "./Upload";
import Preview from "./Preview";
import Parameters from "./Parameters";

export default {
  components: {
    Upload,
    Preview,
    Parameters,
  },
};
</script>
