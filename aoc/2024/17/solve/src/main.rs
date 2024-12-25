use std::fs;

fn run_program(mut a: i64, mut b: i64, mut c: i64, program: &Vec::<i32>) -> Vec::<i32> {
    let mut ip = 0;
    let mut ret = Vec::new();
    while ip < program.len() {
        let arg = program[ip+1] as i64;
        let combo = if arg <= 3 {
            arg
        } else if arg == 4 {
            a
        } else if arg == 5 {
            b
        } else {
            c
        };
        
        match program[ip] {
            0 => {
                if combo == 0 {
                    return ret;
                }
                a /= 2_i64.pow(combo as u32);
                ip += 2;
            },
            1 => {
                b ^= arg;
                ip += 2;
            },
            2 => {
                b = combo % 8;
                ip += 2;
            },
            3 => {
                if a == 0 {
                    ip += 2;
                } else {
                    ip = arg as usize;
                }
            },
            4 => {
                b ^= c;
                ip += 2;
            },
            5 => {
                ret.push((combo % 8) as i32);
                ip += 2;
            },
            6 => {
                if combo == 0 {
                    return ret;
                }
                b = a / 2_i64.pow(combo as u32);
                ip += 2;
            },
            7 => {
                if combo == 0 {
                    return ret;
                }
                c = a / 2_i64.pow(combo as u32);
                ip += 2;
            },
            _ => panic!("bad opcode"),
        }
    }
    ret
}

fn print_output(output: Vec::<i32>) {
    let res = output.iter().map(|n| n.to_string())
        .collect::<Vec::<_>>()
        .join(",");
    println!("{}", res);
}

fn main() {
    let input = fs::read_to_string("input").unwrap();
    let (regs, input) = input.split_once("\n\n").unwrap();
    let [a, b, c]: [i64; 3] = regs
        .lines()
        .map(|l| l.split_once(": ").unwrap().1.parse::<i64>().unwrap())
        .collect::<Vec<_>>().try_into().unwrap();

    let ops = input.split_once(": ").unwrap().1
        .split(",")
        .map(|n| n.parse::<i32>().unwrap())
        .collect::<Vec<_>>();

    // part1
    print_output(run_program(a, b, c, &ops));

    // let mut i = 0;
    // loop {
    //     let out = run_program(i, b, c, &ops);
    //     if i % 10000 == 0 {
    //         println!("{}", i);
    //     }
    //     if out == ops {
    //         println!("{}", i);
    //         break;
    //     }
    //     i += 1;
    // }
}
