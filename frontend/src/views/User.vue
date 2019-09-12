<template>
  <div>
    <h1>Home Page</h1>
    <ToDoList/>
  </div>
</template>

<script>
import ToDoList from '@/components/ToDoList'

export default {
  components: {
    ToDoList
  },
  data () {
    return {
      randomNumber: 0
    }
  }
}
</script>
