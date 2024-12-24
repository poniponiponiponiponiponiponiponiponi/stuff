use std::fs;
use std::cmp;

struct Instance {
    button_a: (i64, i64),
    button_b: (i64, i64),
    prize: (i64, i64)
}

fn parse() -> Vec<Instance> {
    let mut ret = Vec::new();
    for instance in fs::read_to_string("input").unwrap().split("\n\n") {
        let mut iter = instance.lines();
        let button_a = iter.next().unwrap();
        let button_b = iter.next().unwrap();
        let prize = iter.next().unwrap();
        
        let parse_button = |b: &str| {
            let (x, y) = b.split_once(": ").unwrap().1.split_once(", ").unwrap();
            let x = x.split_once("+").unwrap().1.parse::<i64>().unwrap();
            let y = y.split_once("+").unwrap().1.parse::<i64>().unwrap();
            (x, y)
        };
        let (button_a, button_b) = (parse_button(button_a), parse_button(button_b));

        let (prize_x, prize_y) = prize.split_once(": ").unwrap().1
            .split_once(", ").unwrap();
        let prize_x = prize_x.split_once("=").unwrap().1.parse::<i64>().unwrap();
        let prize_y = prize_y.split_once("=").unwrap().1.parse::<i64>().unwrap();
        let prize = (prize_x, prize_y);
        ret.push(Instance { 
            button_a,
            button_b,
            prize
        });
    }

    ret
}

fn part1() {
    let instances = parse();
    let mut ans1 = 0i64;
    for instance in instances {
        let mut table = [[(0, 0); 101]; 101];
        for y in 1..table.len() {
            let (bx, by) = instance.button_b;
            let (tx, ty) = table[y-1][0];
            table[y][0] = (bx+tx, by+ty);
        }
        
        for y in 0..table.len() {
            for x in 1..table[y].len() {
                let (ax, ay) = instance.button_a;
                let (tx, ty) = table[y][x-1];
                table[y][x] = (ax+tx, ay+ty);
            }
        }

        let mut min_cost = i32::MAX;
        for y in 0..table.len() {
            for x in 0..table[y].len() {
                let (xpos, ypos) = table[y][x];
                let (prize_x, prize_y) = instance.prize;
                if xpos == prize_x && ypos == prize_y {
                    let cand = x*3 + y*1;
                    if (cand as i32) < min_cost {
                        min_cost = cmp::min(min_cost, cand as i32);
                    }
                }
            }
        }

        if min_cost != i32::MAX {
            ans1 += min_cost as i64;
        }
    }

    println!("{}", ans1);
}

fn part2() {
    let instances = parse();
    let mut ans1 = 0i64;

    for instance in instances {
        let px = instance.prize.0 + 10_000_000_000_000;
        let py = instance.prize.1 + 10_000_000_000_000;

        let (ax, ay) = instance.button_a;
        let (bx, by) = instance.button_b;
        let a = by * px - bx * py;
        let b = ax * py - ay * px;
        let det = ax * by - ay * bx;
        if a % det != 0 || b % det != 0 {
            continue;
        }
        ans1 += 3 * a/det + b/det;
    }

    println!("{}", ans1);
}

fn main() {
    part2();
}
