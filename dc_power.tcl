# Cale Woodward
try {
    set home_directory [getenv HOME_DIRECTORY]
} on error {msg} {
    puts "ERROR: missing HOME_DIRECTORY environment variable"
    puts "Message: $msg"
    exit 1
}

try {
    set design_path [getenv DESIGN_PATH]
} on error {msg} {
    puts "ERROR: missing DESIGN_PATH environment variable"
    puts "Message: $msg"
    exit 1
}

try {
    set design_name [getenv DESIGN_NAME]
} on error {msg} {
    puts "ERROR: missing DESIGN_NAME environment variable"
    puts "Message: $msg"
    exit 1
}

# library set-up
set search_path     [list ${home_directory}/ref/SAED_EDK90nm/synopsys/]
set target_library  [list saed90nm_typ.db]
set link_library    [list saed90nm_typ.db]

# working directory
define_design_lib work -path ./work

# read files
analyze -format verilog ${design_path}

# set top module and elaborate
set top ${design_name}
elaborate -lib work $top
current_design $top

# resolve design differences and set constraints
link

# compile design
compile

# ungroup & flatten design
set_flatten true
uniquify -force
ungroup -all -flatten

# report power
report_power        >> ${design_name}_power.rpt


exit
