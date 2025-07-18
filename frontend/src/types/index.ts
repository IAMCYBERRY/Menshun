export interface User {
  id: string
  user_principal_name: string
  display_name: string
  given_name?: string
  surname?: string
  email?: string
  department?: string
  job_title?: string
  manager_id?: string
  is_privileged: boolean
  risk_score: number
  last_sign_in?: string
  account_enabled: boolean
  created_date: string
  last_modified: string
  compliance_status: 'compliant' | 'non_compliant' | 'pending'
  certification_due?: string
  tags?: string[]
}

export interface ServiceIdentity {
  id: string
  identity_type: 'service_account' | 'service_principal' | 'managed_identity' | 'workload_identity'
  name: string
  description?: string
  application_id?: string
  object_id?: string
  tenant_id?: string
  subscription_id?: string
  resource_group?: string
  is_enabled: boolean
  risk_score: number
  last_used?: string
  created_date: string
  last_modified: string
  owner_id?: string
  tags?: string[]
}

export interface DirectoryRole {
  id: string
  template_id: string
  role_name: string
  description: string
  category: string
  subcategory?: string
  is_privileged: boolean
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  risk_score: number
  requires_justification: boolean
  requires_approval: boolean
  max_assignment_duration_days?: number
  can_manage_users: boolean
  can_manage_groups: boolean
  can_manage_applications: boolean
  can_manage_devices: boolean
  can_read_directory: boolean
  can_write_directory: boolean
  compliance_frameworks?: string[]
  requires_certification: boolean
  certification_frequency_days?: number
  segregation_of_duties_conflicts?: string[]
  documentation_url?: string
}

export interface RoleAssignment {
  id: string
  user_id?: string
  service_identity_id?: string
  directory_role_id: string
  assignment_type: 'permanent' | 'eligible' | 'time_limited'
  assignment_reason?: string
  justification?: string
  assigned_by: string
  assigned_date: string
  start_date: string
  end_date?: string
  status: 'pending_approval' | 'approved' | 'active' | 'expired' | 'revoked'
  approved_by?: string
  approved_date?: string
  last_activated?: string
  activation_count: number
  created_date: string
  last_modified: string
  compliance_status: 'compliant' | 'non_compliant' | 'pending'
}

export interface Credential {
  id: string
  credential_type: 'password' | 'certificate' | 'secret' | 'key'
  name: string
  description?: string
  vault_path: string
  service_identity_id?: string
  user_id?: string
  is_active: boolean
  expires_at?: string
  last_rotated?: string
  rotation_frequency_days?: number
  auto_rotation_enabled: boolean
  created_date: string
  last_modified: string
  last_accessed?: string
  access_count: number
  tags?: string[]
}

export interface AuditLog {
  id: string
  event_type: string
  event_category: string
  user_id?: string
  service_identity_id?: string
  resource_type: string
  resource_id?: string
  action: string
  result: 'success' | 'failure' | 'partial'
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  source_ip?: string
  user_agent?: string
  location?: string
  details: Record<string, any>
  created_date: string
  correlation_id?: string
}

export interface Session {
  id: string
  user_id: string
  session_token: string
  ip_address?: string
  user_agent?: string
  location?: string
  device_id?: string
  is_active: boolean
  created_date: string
  last_activity: string
  expires_at: string
  security_flags?: string[]
}

export interface DashboardStats {
  total_users: number
  privileged_users: number
  service_identities: number
  active_role_assignments: number
  pending_approvals: number
  high_risk_assignments: number
  compliance_violations: number
  recent_activities: number
}

export interface DashboardMetrics {
  risk_distribution: {
    low: number
    medium: number
    high: number
    critical: number
  }
  assignment_trends: Array<{
    date: string
    assignments: number
    revocations: number
  }>
  compliance_status: {
    compliant: number
    non_compliant: number
    pending: number
  }
  top_roles: Array<{
    role_name: string
    assignment_count: number
    risk_score: number
  }>
}

export interface ApiResponse<T = any> {
  data: T
  success: boolean
  message?: string
  errors?: string[]
}

export interface PaginatedResponse<T = any> {
  data: T[]
  total: number
  page: number
  limit: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

export interface ErrorResponse {
  error: string
  message: string
  details?: Record<string, any>
  timestamp: string
}

export interface FilterOptions {
  search?: string
  filters?: Record<string, any>
  sort_by?: string
  sort_order?: 'asc' | 'desc'
  page?: number
  limit?: number
}

export type RiskLevel = 'low' | 'medium' | 'high' | 'critical'
export type ComplianceStatus = 'compliant' | 'non_compliant' | 'pending'
export type AssignmentType = 'permanent' | 'eligible' | 'time_limited'
export type AssignmentStatus = 'pending_approval' | 'approved' | 'active' | 'expired' | 'revoked'
export type CredentialType = 'password' | 'certificate' | 'secret' | 'key'
export type ServiceIdentityType = 'service_account' | 'service_principal' | 'managed_identity' | 'workload_identity'
export type EventResult = 'success' | 'failure' | 'partial'