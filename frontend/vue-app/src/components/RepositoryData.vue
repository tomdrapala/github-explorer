<!-- 
In this situation, it probably doesn't make sense to implement the repositories list as a separate component,
so this component is not used, but I am leaving it just for reference.
-->
<template>
    <li>
        <h3>{{ name }}</h3>
        <ul>
            <li><b>Description:</b> {{ description }}</li>
            <li><b>Stars:</b> {{ stars }}</li>
        </ul>
    </li>
</template>

<script>
export default ({
    props: {
        name: {type: String, required: true},
        description: {type: String, required: false},
        stars: {type: Number, required: false},
    }
})
</script>
