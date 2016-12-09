#!/usr/bin/env bats
load test_helper

setup() {
    clean_storage || true
}

@test "hosts help by arg" {
    run termius hosts --help
    [ "$status" -eq 0 ]
}

@test "hosts help command" {
    run termius help hosts
    [ "$status" -eq 0 ]
}

@test "List hosts in table format" {
    termius host -L test --port 2022 --address 123.2.3.2 --username root --password password
    run termius hosts
    [ "$status" -eq 0 ]
    [ $(get_models_set_length 'host_set') -eq 1 ]
}

@test "List hosts filter by tag" {
    termius host -L test --port 2022 --address localhost --username root --password password
    host_id=$(termius host -L test --port 2022 --address localhost --username root --password password -t A)

    run termius hosts --tag A -f csv -c id
    [ "$status" -eq 0 ]
    [ "${lines[1]}" = "$host_id" ]
    [ "${lines[2]}" = "" ]
    [ $(get_models_set_length 'host_set') -eq 2 ]
}

@test "List hosts in group" {
    group=$(termius group --port 2022)
    host_id=$(termius host -L test --group $group --address localhost --username root --password password)

    run termius hosts --group $group -f csv -c id
    [ "$status" -eq 0 ]

    [ "${lines[1]}" = "$host_id" ]
    [ "${lines[2]}" = "" ]
    [ $(get_models_set_length 'host_set') -eq 1 ]
}

@test "List hosts in group filter by tag" {
    group=$(termius group --port 2022)
    host_id=$(termius host -L test --group $group --address localhost --username root --password password -t A)
    termius host -L test --address localhost --username root --password password -t A

    run termius hosts --tag A --group $group -f csv -c id
    [ "$status" -eq 0 ]
    [ "${lines[1]}" = "$host_id" ]
    [ "${lines[2]}" = "" ]
    [ $(get_models_set_length 'host_set') -eq 2 ]
}
