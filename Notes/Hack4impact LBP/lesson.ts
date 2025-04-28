let student = 'smart'
console.log(student)

student = 'genius'
console.log(student)


const person = 'fluffy'
const jobtitle = 'comedian'
console.log(`${person} is the funniest ${jobtitle} allive`)

const goals = ['become a dood dev' , ' and have fun']
goals.push('stay hydrated')
console.log(goals)

const teacher = {

    name: 'judah',
    age: '19'
}

interface UTstudent{
    name: string;
    gpa: number;
    major ?: string;
}
const judah: UTstudent = {name: "judah", gpa:0.0 }
console.log(judah)

function helloworld(name: string): string{
    return`hellow ${name}!`

}
console.log(helloworld('judah'))


