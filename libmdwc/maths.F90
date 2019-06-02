module maths

 use parameters

implicit none

contains

	subroutine cross_product(a,b,crossp)
	 !a very simple implementation of the cross product
		  implicit none
		  real(8),intent(in) ::a(3),b(3)
		  real(8),intent(out)::crossp(3)

		  crossp(1)=a(2)*b(3)-a(3)*b(2)
		  crossp(2)=a(3)*b(1)-a(1)*b(3)
		  crossp(3)=a(1)*b(2)-a(2)*b(1)
		  return
	end subroutine cross_product

	subroutine invertmat(mat,matinv,n)
          implicit none
	  integer,intent(in) :: n
	  real(8),intent(in) :: mat(n,n)
	  real(8),intent(out)   :: matinv(n,n)
	  real(8)               :: a(n,n),div
	  !Here only for a 3*3 matrix
	  a=mat
	  div=(a(1,1)*a(2,2)*a(3,3)-a(1,1)*a(2,3)*a(3,2)-a(1,2)*a(2,1)*a(3,3)+a(1,2)*a(2,3)*a(3,1)+&
	  &a(1,3)*a(2,1)*a(3,2)-a(1,3)*a(2,2)*a(3,1)) 
	  div=1.d0/div
	  matinv(1,1) = (a(2,2)*a(3,3)-a(2,3)*a(3,2))*div
	  matinv(1,2) =-(a(1,2)*a(3,3)-a(1,3)*a(3,2))*div
	  matinv(1,3) = (a(1,2)*a(2,3)-a(1,3)*a(2,2))*div
	  matinv(2,1) =-(a(2,1)*a(3,3)-a(2,3)*a(3,1))*div
	  matinv(2,2) = (a(1,1)*a(3,3)-a(1,3)*a(3,1))*div
	  matinv(2,3) =-(a(1,1)*a(2,3)-a(1,3)*a(2,1))*div
	  matinv(3,1) = (a(2,1)*a(3,2)-a(2,2)*a(3,1))*div
	  matinv(3,2) =-(a(1,1)*a(3,2)-a(1,2)*a(3,1))*div
	  matinv(3,3) = (a(1,1)*a(2,2)-a(1,2)*a(2,1))*div
	  return
	end subroutine invertmat

	subroutine rotation(rotmat,angle,axe)
		!This subroutine will calculate the rotational matrix rotmat for a
		!3-dim vector around an axis 'axe' by the angle 'angle'.
		implicit none
		real(8),intent(in) :: angle
		real(8),intent(in) :: axe(3)
		real(8):: rotator(3,3)
		real(8):: rotmat(3,3)

		!Define Rotation Matrix
		rotator(1,1)=dcos(angle)+(axe(1)**2)*(1.d0-dcos(angle))
		rotator(1,2)=axe(1)*axe(2)*(1.d0-dcos(angle))-axe(3)*dsin(angle)
		rotator(1,3)=axe(1)*axe(3)*(1.d0-dcos(angle))+axe(2)*dsin(angle)

		rotator(2,1)=axe(2)*axe(1)*(1.d0-dcos(angle))+axe(3)*dsin(angle)
		rotator(2,2)=dcos(angle)+(axe(2)**2)*(1.d0-dcos(angle))
		rotator(2,3)=axe(2)*axe(3)*(1.d0-dcos(angle))-axe(1)*dsin(angle)

		rotator(3,1)=axe(3)*axe(1)*(1.d0-dcos(angle))-axe(2)*dsin(angle)
		rotator(3,2)=axe(3)*axe(2)*(1.d0-dcos(angle))+axe(1)*dsin(angle)
		rotator(3,3)=dcos(angle)+(axe(3)**2)*(1.d0-dcos(angle))
		rotmat(:,:)=rotator(:,:)

		!do i=1,3
		!   vector2(i)=rotator(i,1)*vector(1)+rotator(i,2)*vector(2)+rotator(i,3)*vector(3)
		!enddo
		!vector(:)=vector2(:)
	end subroutine rotation

	subroutine gausdist(nat,vel_in)
		!generates 3*nat random numbers distributed according to  exp(-.5*vel_in**2)
		implicit none
		integer, intent(in) :: nat
		real(8), dimension(3,nat), intent(out) :: vel_in
		!temporal storage
		real:: s1,s2
		real(8):: t1,t2,tt
		! On Intel the random_number can take on the values 0. and 1.. To prevent overflow introduce eps
		real(8),dimension(3*nat)::  vxyz
		integer:: i,j
		do i=1,3*nat-1,2
			call random_number(s1)
			t1=eps+(1.d0-2.d0*eps)*dble(s1)
			call random_number(s2)
			t2=dble(s2)
			tt=sqrt(-2.d0*log(t1))
			vxyz(i)=tt*cos(twopi*t2)
			vxyz(i+1)=tt*sin(twopi*t2)
		enddo
		call random_number(s1)
		t1=eps+(1.d0-2.d0*eps)*dble(s1)
		call random_number(s2)
		t2=dble(s2)
		tt=sqrt(-2.d0*log(t1))
		vxyz(3*nat)=tt*cos(twopi*t2)
		!call elim_moment(nat,vel_in,amass)
		do j=1, nat
			do i=1, 3
				vel_in(i,j)= vxyz(3*(j-1) + i)
			end do
		end do
		return
	end subroutine gausdist

    subroutine gausdist_cell(vel_lat_in)
		! generates 3*3 random numbers distributed according to  exp(-.5*vxyz**2) for the cell vectors
		implicit none
		!real(8), dimension(3,3), intent(in) :: latvec_in
		real(8), dimension(3,3), intent(out) :: vel_lat_in
		!real(8), dimension(3,3), intent(out) :: vel_lat_in
		integer:: i,j
		real:: s1,s2
		real(8) :: t1,t2,tt
		! On Intel the random_number can take on the values 0. and 1.. To prevent overflow introduce eps
		real(8)::  vlat(9)

		do i=1,3*3-1,2
			call random_number(s1)
			t1=eps+(1.d0-2.d0*eps)*dble(s1)
			call random_number(s2)
			t2=dble(s2)
			tt=sqrt(-2.d0*log(t1))
			vlat(i)=tt*cos(twopi*t2)
			vlat(i+1)=tt*sin(twopi*t2)
		enddo
		call random_number(s1)
		t1=eps+(1.d0-2.d0*eps)*dble(s1)
		call random_number(s2)
		t2=dble(s2)
		tt=sqrt(-2.d0*log(t1))
		vlat(3*3)=tt*cos(twopi*t2)
		do j=1, 3
			do i=1, 3
				vel_lat_in(i,j)= vlat(3*(j-1) + i)
			end do
		end do
		!call elim_torque_cell(latvec_in,vel_lat_in)
		return
    end subroutine gausdist_cell
    
end module maths
