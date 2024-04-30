# Cale Woodward
try {
    set home_directory [getenv HOME_DIRECTORY]
} on error {msg} {
    puts "ERROR: missing HOME_DIRECTORY environment variable"
    puts "Message: $msg"
    exit 1
}

try {
    set design_directory [getenv DESIGN_DIRECTORY]
} on error {msg} {
    puts "ERROR: missing DESIGN_DIRECTORY environment variable"
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
define_design_lib work -path ./{$design_name}_work

# read files
#analyze -format verilog ${design_path}
analyze -autoread -recursive ${design_directory} -top ${design_name}

# set top module and elaborate
elaborate -lib work ${design_name}
current_design ${design_name}

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
