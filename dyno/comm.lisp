(uart-start 115200)
(loopwhile t
    (progn
        (uart-write "Hey")
        (sleep 1)
    )
)
