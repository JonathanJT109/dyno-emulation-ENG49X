;; Constant
(define *D_t* 0.3) ; Kart tire diameter in meters
(define *Gr* (/ 13.0 55)) ; Gearing ratio
(define *P* 1.0) ; Tire pressure (barr)
(define *rho* 1.2) ; Air density (kg/m^3)
(define *m* 200.0) ; Kart mass (kg)
(define *g* 9.8) ; Gravity acceleration constant (m/s^2)
(define *C_d* 0.8) ; Drag coefficient (unitless)
(define *A* 0.5) ; Maximum cross-sectional area (m^2)
(define +pi+ 3.14159)
(define prev-v 0.0)
(define response-rate 0.1)
(define *mu_s* 0.8) ; Static Friction coefficient

(define a (* -0.99 *g* *mu_s*))
(define dec (* a (/ 6 (* *D_t* *Gr*)))) ;rps per second * res


;; Braking force
(defun rpm-to-rps (rpm)
  (/ rpm 60))

(defun rpm-to-v (rpm)
  (let ((rps (rpm-to-rps rpm)))
    (* *Gr* rps +pi+ *D_t*)))

(define braking-force
  (lambda (rpm dvdt)
    (let ((v (rpm-to-v rpm))
          (term1-1 (/ (* 3.6 v) 100.0))
          (term1-2 (+ 0.01 (* 0.0095 (* term1-1 term1-1))))
          (term1-3 (+ 0.005 (* (/ 1 *P*) term1-2)))
          (term1 (* term1-3 *m* *g*))
          (term2 (/ (* *C_d* *A* *rho* (* v v)) 2))
          (term3 (* *m* dvdt))
          (result (+ term1 term2 term3)))  ;; Correctly defining `result`
      result)))  ;; Returning `result`

(define deacceleration
  (lambda ( ) ))

(define get-dvdt
  (lambda (curr-rpm)
    (let ((curr-v (rpm-to-v curr-rpm))
          (term-1 (- curr-v prev-v))
          (result (/ term-1 response-rate)))
      (setvar 'prev-v curr-v)
      result)))

(define make-list
    (lambda (n val)
    (if (= n 0)
        nil
        (cons val (make-list (- n 1) val))
    )
    ))

(define queue-size 10) ;; Can be modified

(define lsum
    (lambda (lst)
    (eval (cons '+ lst))))

(define nq
    (lambda (lst ele)
        (append (rest lst) (list ele))))

(define get-avg
    (lambda (lst)
        (/ (lsum lst) (to-float (length lst)))
    ))

(define q (make-list queue-size 0))

(print "")
(print "Start")

(define i 0)
(loopwhile (< i 5)
    (progn
    (set-rpm 3000)
    (sleep 1)
    (define i (+ i 1))
    ))

(defun main ()
    (loopwhile t
        (progn
        (if (eq 'l-min-erpm -1)
            (let ((rpm (/ (get-rpm) 3.0))
                  (new-rpm (* 3 (- dec rpm)))) ; TODO
                  (progn
                    (if (> new-rpm 0)
                       (set-rpm new-rpm)
                    )
                    (print (str-merge "RPM: " (str-from-n rpm)))
                  )
            )
            (let ((rpm (/ (get-rpm) 3.0))
                  (dv-dt (get-dvdt rpm))
                  (bf (braking-force rpm dv-dt))
                  (bf-amps (/ bf (get-vin)))
                  (output (str-merge "RPM: " (str-from-n rpm) " | BF (W): " (str-from-n bf) " | BF (A): " (str-from-n bf-amps))))
                (progn
                    (setvar 'q (nq q bf-amps))
                    (set-brake (get-avg q))
                    (print output)
                )
            )
        )
        (sleep response-rate)
        )))

(main)

